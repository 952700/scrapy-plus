# _*_ coding:utf-8 _*_


# 导入URL规范化函数
from w3lib.url import canonicalize_url # 需要再requirements.txt添加依赖
# 导入hashlib
import hashlib
import six
from ..utils.log import logger
from ..conf import settings
"""
调度器模块
1. 缓存请求对象
2. 请求去重

# 3.2.1-根据配置文件, 是否需要对象请求和指纹进行持久化
1. 如果不需要持久化, 导入内存的队列和去重容器, 否则就导入基于Redis队列和去重容器
2. 修改init方法, 创建去重容器
3. 修改seen_request方法,该为使用去重容器的接口

"""
# 1. 如果不需要持久化, 导入内存的队列和去重容器, 否则就导入基于Redis队列和去重容器
if not settings.SCHEDULE_PERSIST:
    # six是专门用于进行python2和python3的兼容的
    from six.moves.queue import Queue
    from ..utils.set import NormalFilterContainer as FilterContainer
else:
    # 导入基于Redis队列
    from ..utils.queue import Queue
    from ..utils.set import RedisFilterContainer as FilterContainer

class Scheduler(object):

    def __init__(self, stats_collector):
        #  3.2.1-3: 调度器中接收统计器对象, 使用统计器对象, 对入队请求数量和过滤掉请求数量进行统计
        self.stats_collector = stats_collector

        # 准备队列, 来缓存请求对象
        self.queue = Queue()
        #  2.0.2-5: 统计总的请求数量
        # self.total_request_count = 0
        # 定义set集合, 用于存储指纹数据
        # 2. 修改init方法, 创建去重容器
        self.filter_container = FilterContainer()
        # 定义变量, 用于统计过滤掉多少请求
        # self.filter_reqeust_count = 0

    def clear(self):
        """请求Redis中的指纹和请求数据"""
        if settings.SCHEDULE_PERSIST:
            # 清空Redis队列中数据
            self.queue.clear()
            # 请求空指纹数据
            self.filter_container.clear()

    def add_request(self, request):
        #  3.2.1-4: 使用stats_collector来通过入队请求数量和过滤掉请求数量
        #  3.3.1-2: 只有需要过滤 并且 已经重复, 才过滤
        if not request.dont_filter and self.seen_request(request):
            # 如果重复, 就记录日志
            logger.info('过滤掉重复请求:{}'.format(request.url))
            # self.filter_reqeust_count += 1
            self.stats_collector.incr_filter_request_count()
            return

        # print(request.url)
        # 添加请求对象
        self.queue.put(request)
        # print('添加请求:{}'.format(request.url))
        # 2.0.2-5: 每次添加请求的时候, 就让total_request_count增加1
        # 此处请求数量, 为入队请求数量
        # self.total_request_count += 1
        self.stats_collector.incr_total_request_count()

    def get_request(self):
        # print("获取请求")
        # 获取请求对象
        req = self.queue.get()
        # print("取出了:{}".format(req.url))
        return req

    def seen_request(self, request):
        # 用于爬虫请求是否已经爬取过了, 待实现
        # 根据请求获取该请求对应指纹
        fp = self._gen_fp(request)
        # 判断fp是否在容器中
        if self.filter_container.exists(fp):
            # 返回True,说明这个请求重复了
            return True

        # 如果不重复就来到这里, 把指纹添加过滤容器中
        self.filter_container.add_fp(fp)
        # 返回False, 就表示不重复
        return False

    def _gen_fp(self, request):
        """
        根据请求对象, 生成指纹
        :param request: 请求对象
        :return: 请求对应指纹
        思路:
         1. 明确需要使用那些数据生成指纹
            1. URL,方法名,params,data
         2. 准备数据
         3. 把数据添加到sha1算法中
         4. 通过sha1获取16进制的指纹
        """
        # 2. 准备数据
        # 对URL进行规范化处理
        url = canonicalize_url(request.url)
        # 方法名
        method = request.method.upper()
        # GET的请求参数
        params = request.params if request.params else {}
        # 但是字典是无序, 我们把转换为元祖在排序
        params = sorted(params.items(), key=lambda x: x[0])

        # POST请求的请求体数据
        data = request.data if request.data else {}
        # 但是字典是无序, 我们把转换为元祖在排序
        data = sorted(data.items(), key=lambda x: x[0])

        # 3. 获取sha1算法对象
        sha1 = hashlib.sha1()
        # 更新数据
        sha1.update(self.get_bytes_from_str(url))
        sha1.update(self.get_bytes_from_str(method))
        sha1.update(self.get_bytes_from_str(str(params)))
        sha1.update(self.get_bytes_from_str(str(data)))

        # 获取十六进制的指纹数据
        return sha1.hexdigest()


    def get_bytes_from_str(self, s):
        if six.PY3:
            # 如果是py3, 如果是str类型就需要进行编码
            if isinstance(s, str):
                return s.encode('utf8')
            else:
                return s
        else:
            # 如果是py2, 如果是str类型就直接返回
            if isinstance(s, str):
                return s
            else:
                # 在py2中encode默认使用ascii码进行编码的,此处不能省
                return s.encode('utf8')