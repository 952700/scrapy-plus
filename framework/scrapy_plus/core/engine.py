# _*_ coding:utf-8 _*_

from collections import Iterable
import importlib

from ..conf import settings

# 2. 在引擎中,如果线程版, 就导入线程池, 如果是协程版, 就导入协程池
if settings.ASYNC_TYPE.lower() == 'thread':
    from multiprocessing.dummy import Pool
else:
    from ..async.coroutine import Pool


# 3.2.1: 如果不需持久化, 就导入的内存存储统计器类, 否则就导入Redis版的统计器类
if not settings.SCHEDULE_PERSIST:
    from ..utils.stats_collector import NormalStatsCollector as StatsCollector
else:
    from ..utils.stats_collector import RedisStatsCollector as StatsCollector

import time
from .downloader import Downloader
from .scheduler import Scheduler
from ..http.request import Request
from ..items import Item

from ..utils.log import logger
from datetime import datetime

"""
引擎模块: 负责协调各个模块
1. 框架启动
2. 框架运行流程

思路:
 1. 对各个模块进行初始化
 2. 启动爬虫, 实现运行逻辑
 
# 1.2 版本
  - 1. 增加一个utils -> log.py
  - 2. 在引擎的start方法输出引擎的启动时间, 结束时间, 总耗时
 
3.0.1: 实现线程池的异步任务(雏形版)
- 1. 在init方法中创建线程池对象
- 2. 在start方法中分分别使用异步任务执行add_start_request和execute_request_response_item
- 3. 把execute_request_response_item死循环调用该为callback循环调用
 
3.0.2: 通过配置文件来控制异步任务数量
- 1. 修改default_settings.py增加异步任务个数配置
- 2. 修改引擎执行异步任务的方法, 配置了几个异步任务, 我们就开几个异步任务来执行execute_request_xxx
 
3.0.3: 线程的异常处理; 在线程任务内部的异常无法直接传到主线线程, 所以导致线程内部报错, 而我们也不知道, 怎么办?
- 在线程执行异步任务的时候支持错误回调, 它会把出错信息, 通过该函数告知我们
1. 写一个错误回调函数
2. 在调用异步任务的时候, 传入该错误回调函数

3.1 协程池的实现
1. 在配置文件中, 配置异步类
2. 在引擎中,如果线程版, 就导入线程池, 如果是协程版, 就导入协程池

# 3.2.1: 如果不需持久化, 就导入的内存存储统计器类, 否则就导入Redis版的统计器类
  3.2.1-2: 在init方法中, 创建统计器对象, 传入到调度器中
  3.2.1-3: 调度器中接收统计器对象, 使用统计器对象, 对入队请求数量和过滤掉请求数量进行统计
  3.2.1-5: 使用统计器类来统计总响应处理数量
  3.2.1-7: 修改结束爬虫条件, 使用统计器中数据进行判断
  3.2.1-8: 在统计信息输出时候, 都使用统计器中的数据.
  
3.3.3: 问题- 还有爬虫在不断构造请求, 但是整个程序退出了
解决: 
 1. 在init方法, 定义一个变量, 用于记录已经添加完毕起始请求的爬虫个数
 2. 在执行添加一个爬虫的回调函数中, 让这个变量 +=1
 3. 在判断结束添加时候, 如果已经添加完毕起始请求的爬虫个数 >= 总爬虫个数, 才去判断结束条件
"""


class Engine(object):

    # 2.0.1-2: 在初始化方法中, 增加爬虫参数, 接收项目中传入的爬虫对象
    # 2.2-1: 接收spiders字典, key是爬虫名称, 值爬虫对象
    # 2.3.7 - 增加pipelines参数, 接收管道列表
    # 2.4-4: 接收爬虫中间件列表和下载中间件列表
    def __init__(self):
        # 3.0.1: 实现线程池的异步任务(雏形版)
        # - 1. 在init方法中创建线程池对象
        self.pool = Pool()

        # 初始四大核心模块
        # 2.5.5; 修改init方法, 根据配置动态创建就爬虫,管道,中间件对象列表
        self.spiders = self.auto_import(settings.SPIDERS, True)
        #  3.2.1-2: 在init方法中, 创建统计器对象, 传入到调度器中
        self.stats_collector = StatsCollector(self.spiders.keys())
        # 把统计器类传入到调度器中
        self.scheduler = Scheduler(self.stats_collector)


        self.downloader = Downloader()

        # 2.3.7 - 修改pipeline为pipelines, 接收传入的pipelines
        self.pipelines = self.auto_import(settings.PIPELINES)
        # 1.1-1 初始爬虫中间件和下载器中间件
        # self.spider_middleware = SpiderMiddleware()
        # self.downloader_middleware = DownloaderMiddleware()

        # 2.4-5: 接收爬虫中间件列表和下载中间件列表
        self.spider_middlewares = self.auto_import(settings.SPIDER_MIDDLEWARES)
        self.downloader_middlewares = self.auto_import(settings.DOWNLOADER_MIDDLEWARES)

        #  2.0.2-6: 统计总的响应处理数量
        # self.total_response_count = 0
        #  3.3.3-1. 在init方法, 定义一个变量, 用于记录已经添加完毕起始请求的爬虫个数
        self.finished_start_request_spider_count = 0

    def auto_import(self, full_names, is_spider=False):
        """
        2.5.6: 实现动态导入方法
        :param full_names: 类全名类别
        :param is_spider: 是否是爬虫
        :return: 如果是爬虫,就返回一个字典, 否则就返回一个列表
        """
        # 如果是爬虫,就返回一个字典, 否则就返回一个列表
        results = {} if is_spider else []

        # 遍历full_names获取类全名
        for full_name in full_names:
            # 截取获取模块名和类名
            split_names = full_name.rsplit('.', maxsplit=1)
            module_name = split_names[0]
            class_name = split_names[1]

            # 动态导入模块, 获取模块对象
            module = importlib.import_module(module_name)
            # 使用模块对象,根据类名获取类对象
            cls = getattr(module, class_name)
            # 使用类对象, 创建实例对象
            instance = cls()
            # 如果是爬虫, 就给字典赋值, key就是爬虫名称, 值就是爬虫对象
            if is_spider:
                results[instance.name] = instance
            else:
                # 否则就添加到列表中
                results.append(instance)
        # 返回结果
        return results

    def start(self):
        # 对外提供启动接口
        # 为了代码的可扩展新, 在内部封装为一个私有方法来实现核心逻辑
        #   - 2. 在引擎的start方法输出引擎的启动时间, 结束时间, 总耗时
        start_time = datetime.now()
        logger.info('开始时间:{}'.format(start_time))
        self._start()
        end_time = datetime.now()
        # 打印统计信息
        logger.info("总入队请求数量:{}".format(self.stats_collector.total_request_count))
        logger.info("过滤掉请求数量:{}".format(self.stats_collector.filter_request_count))
        logger.info("总响应处理数量:{}".format(self.stats_collector.total_response_count))
        logger.info("起始请求数量数量:{}".format(self.stats_collector.start_request_count))
        logger.info('结束时间:{}'.format(end_time))
        logger.info('总耗时: {}s'.format((end_time-start_time).total_seconds()))

        # 如果是分布式并且不要断点续爬
        if settings.SCHEDULE_PERSIST and not settings.FP_PERSIST:
            # 我们就请求指纹,请求,统计器中的数据 全不清空
            self.scheduler.clear()
            self.stats_collector.clear()

    #1. 写一个错误回调函数
    def error_callback(self, ex):
        """异步的错误回调函数"""
        try:
            raise ex
        except Exception as ex:
            logger.exception(ex)


    def execute_callback(self, temp):
        """执行execute_request_response_item回调函数, 实现循环调用"""
        self.pool.apply_async(self.execute_request_response_item, callback=self.execute_callback, error_callback=self.error_callback)

    def _start(self):

        # 2. 在调用异步任务的时候, 传入该错误回调函数

        # 2.0.2-3: 把添加请求和处理请求拆分为不同的方法
        # 把初始请求添加到调度器中
        self.pool.apply_async(self.add_start_reqeusts, error_callback=self.error_callback)

        # - 2. 修改引擎执行异步任务的方法, 配置了几个异步任务, 我们就开几个异步任务来执行execute_request_xxx
        for i in range(settings.ASYNC_COUNT):
            # 使用异步任务来执行
            self.pool.apply_async(self.execute_request_response_item, callback=self.execute_callback, error_callback=self.error_callback)

        #  2.0.2-4:让方法不断执行, 直到把所有请求都处理完了, 才停止
        # 添加了一个while True程序就不会结束了, 为了能够结束我们就需要知道什么时候请求处理完了
        # 当请求数量和处理请求的数量一样的时候, 就说明处理完毕了
        while True:
            # 让程序稍微休息下, 在判断, 提高效率, 减少cpu消耗
            time.sleep(0.01)

            # 3.3.3-3: 只有已经结束执行添加起始请求任务的爬虫个数 >= 总的爬虫个数, 才判断后续是否结束
            # print("结束爬虫个数:{}".format(self.finished_start_request_spider_count))
            # print("爬虫总个数:{}".format(len(self.spiders)))
            if self.finished_start_request_spider_count >= len(self.spiders):
                # 2.0.2-8: 直到把所有请求都处理完了, 才停止
                # 为了防止万一跑过了, 也能停止.
                # 3.0.1-2: 当使用异步任务的时候, 异步任务可能比主线要慢, 异步任务还没有执行就在这判断了, 次数请求数量和响应数据都是0
                # print("请求数量:{}".format(self.stats_collector.total_request_count))
                # print("响应数量:{}".format(self.stats_collector.total_response_count))
                # 为了解决这个问题, 当响应的处理数量不为0的时候, 才结束
                if self.stats_collector.total_response_count != 0 and self.stats_collector.total_response_count >= self.stats_collector.total_request_count:
                    break

    def execute_request_response_item(self):
        # 1 / 0
        # 3. 获取调度器中的请求对象
        request = self.scheduler.get_request()

        try:
            # 2.2-5: 获取处理该请求对应爬虫
            spider = self.spiders[request.spider_name]

            # 2.4-8: 遍历下载器中间列表, 获取每一个下载器中间件,来处理数据
            for downloader_middleware in self.downloader_middlewares:
                # 1.1-3: 下载器中间件处理请求
                request = downloader_middleware.process_request(request)


            # 4. 把请求对象, 交个下载器, 获取响应数据
            response = self.downloader.get_response(request)

            # 2.1.2-5: 把请求中meta参数, 传递到响应数据中
            response.meta = request.meta

            # 2.4-9: 遍历下载器中间列表, 获取每一个下载器中间件,来处理数据
            for downloader_middleware in self.downloader_middlewares:
                # 1.1.4: 下载器中间件处理响应数据
                response = downloader_middleware.process_response(response)

            # 2.4.5: 遍历爬虫中间件列表, 获取爬虫中间件, 对数据进行处理
            for spider_middleware in self.spider_middlewares:
                # 1.1.5: 爬虫中间件处理响应数据
                response = spider_middleware.process_response(response)

            # 5. 让爬虫处理响应数据
            # 2.1.2-4: 如果请求中有callback就使用callback进行解析, 如果没有就是使用parse函数进行解析
            if request.callback:
                results = request.callback(response)
            else:
                # 2.1.2-2; 处理parse方法返回多结果
                # 2.2-6: 使用请求对应爬虫就该请求的响应数据进行处理
                results = spider.parse(response)

            # 返回结果可能是可以迭代, 也可能不能迭代, 如果不能迭代, 就把变成迭代的, 后面就可以统一处理了
            if not isinstance(results, Iterable):
                results = [results]

            for result in results:
                # 判断这个是数据还是请求
                # 如果是请求, 就添加到调度器中
                if isinstance(result, Request):
                    # 2.2-4: 给request赋值爬虫的名称
                    # 把请求请求的爬虫名称赋值给从解析处理的请求对象中
                    result.spider_name = request.spider_name

                    # 2.4.6: 遍历爬虫中间件列表, 获取爬虫中间件, 对数据进行处理
                    for spider_middleware in self.spider_middlewares:
                        # 1.1-6: 爬虫中间件处理请求数据
                        result = spider_middleware.process_request(result)

                    self.scheduler.add_request(result)
                elif isinstance(result, Item):
                    # 如果是数据交给Pipeline处理
                    # 2.3.8-遍历piplines列表, 对Item进行处理
                    for pipeline in self.pipelines:
                        # 下一个管道,要能够使用上一个管道处理的数据
                        result = pipeline.process_item(result, spider)
                else:
                    raise Exception('爬虫返回的数据必须是Request和Item')
        finally:
            # 2.0.7: 无论处理是否成功, 都要处理数量+1
            # self.total_response_count += 1
            self.stats_collector.incr_total_response_count()

    def add_a_spider_start_requests_callback(self, temp):
        # 3.3.3-2: 让已经结束的添加初始请求的爬虫个数累增1
        self.finished_start_request_spider_count += 1

    def add_start_reqeusts(self):
        # 1. 调用爬虫的strat_reqeusts方法, 获取初始请求对象
        # 2.0.2-3: start_requests是一个Request对象生成器, 修改这里来支持他
        # 2.2-2: 遍历爬虫字典, 取出爬虫名和爬虫对象

        # 3.3.2:问题: 由于前面是一个无限循环的start_requests, 永远都不会结束, 所以后面的爬虫就没有机会执行了
        # 解决: 把执行每一个爬虫添加起始请求到调度器中, 抽取一个方法, 使用异步调用
        for spider_name, spider in self.spiders.items():
           # 异步调用添加一个爬虫起始请求的任务
           self.pool.apply_async(self.add_a_spider_start_requests,args=(spider, spider_name,),
                                 callback=self.add_a_spider_start_requests_callback,
                                 error_callback=self.error_callback)

    def add_a_spider_start_requests(self, spider, spider_name):
        """添加一个爬虫的起始请求,到调度器中"""
        for request in spider.start_requests():
            # 2.2-3: 给request赋值爬虫的名称
            request.spider_name = spider_name

            # 2.4.7: 遍历爬虫中间件列表, 获取爬虫中间件, 对数据进行处理
            for spider_middleware in self.spider_middlewares:
                # 1.1-2: 爬虫中间件处理请求
                request = spider_middleware.process_request(request)
            # print(spider_name)
            # print(request.url)
            # 2. 把该请求对象添加到调度器中
            # 3.2.1-6: 统计起始请求数量
            self.stats_collector.incr_start_request_count()
            self.scheduler.add_request(request)
