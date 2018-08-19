"""
目的: 为了统计入对请求总数量, 处理响应的总数量, 过滤掉的请求的数量, 起始请求的数量
定义两个版本:
  1. 内存版的统计器类
     - 使用字典存储上面的信息

  2. 基于Redis统计器类
    - 使用多个key来分别存储上面的信息
"""


class BasicStatsCollector(object):

    def __init__(self, spider_names):
        """
        用于初始数据, 当框架启动的爬虫不一样,用于统计key就应该是不一样的.
        :param spider_names: 当前系统启动的爬虫名称列表
        """

        # 准备存储数据需要使用key
        # 存储总请求数量的key
        self.total_request_count_key = '_'.join(spider_names)+"_total_request_count_key"
        # 存储总响应处理数量的key
        self.total_response_count_key = '_'.join(spider_names)+"_total_response_count_key"
        # 存储过滤掉请求数量的key
        self.filter_request_count_key = '_'.join(spider_names)+"_filter_request_count_key"
        # 存储起始请求数量的key
        self.start_request_count_key = '_'.join(spider_names) + "_start_request_count_key"

    def incr(self, key):
        """让指定key数量递增1"""
        pass

    def get(self, key):
        pass

    def incr_total_request_count(self):
        self.incr(self.total_request_count_key)

    def incr_total_response_count(self):
        self.incr(self.total_response_count_key)

    def incr_filter_request_count(self):
        self.incr(self.filter_request_count_key)

    def incr_start_request_count(self):
        self.incr(self.start_request_count_key)

    @property
    def total_request_count(self):
        return self.get(self.total_request_count_key)

    @property
    def total_response_count(self):
        return self.get(self.total_response_count_key)

    @property
    def filter_request_count(self):
        return self.get(self.filter_request_count_key)

    @property
    def start_request_count(self):
        return self.get(self.start_request_count_key)


class NormalStatsCollector(BasicStatsCollector):

    def __init__(self, spider_names):
        """
        用于初始数据, 当框架启动的爬虫不一样,用于统计key就应该是不一样的.
        :param spider_names: 当前系统启动的爬虫名称列表
        """

        # 调用服了的初始方法
        super().__init__(spider_names)

        # 准备字典存储相关数据
        self._stats_collector = {
            self.total_request_count_key:0,
            self.total_response_count_key:0,
            self.filter_request_count_key:0,
            self.start_request_count_key:0
        }

    def incr(self, key):
        """让指定key数量递增1"""
        self._stats_collector[key] += 1

    def get(self, key):
        return self._stats_collector.get(key)


from ..conf.settings import REDIS_HOST, REDIS_PORT, REDIS_DB
import redis

class RedisStatsCollector(BasicStatsCollector):

    def __init__(self, spider_names,host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB):
        """
        用于初始数据, 当框架启动的爬虫不一样,用于统计key就应该是不一样的.
        :param spider_names: 当前系统启动的爬虫名称列表
        """

        # 准备存储数据需要使用key,调用父类的init
        super().__init__(spider_names)

        # 链接redis数据库
        self.redis = redis.StrictRedis(host=host, port=port, db=db)

    def incr(self, key):
        """让指定key数量递增1"""
        # 让指定的key的值递增1, 如果没有第一次递增后就是1
        self.redis.incr(key)

    def get(self, key):
        rs = self.redis.get(key)
        # 如果没有数据就是None
        if not rs:
            return 0
        else:
            # 如果有数据, 就转换为int在返回
            return int(rs)

    def clear(self):
        """请求Redis中所有统计信息"""
        self.redis.delete(
            self.total_request_count_key,
            self.total_response_count_key,
            self.filter_request_count_key,
            self.start_request_count_key
        )

