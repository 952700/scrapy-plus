"""实现去重容器"""


class BasicFilterContainer(object):

    def add_fp(self, fp):
        """把指纹数据添加到容器中"""
        pass

    def exists(self, fp):
        """用于判断该指纹是否存在"""
        pass


class NormalFilterContainer(BasicFilterContainer):

    def __init__(self):
        """内存版去重容器, 使用set集合存储指纹数据"""
        # filter_container:公共的
        # _filter_container 受保护的 不能通过 from xxx import * 进行导入
        # __filter_container: 私有, 只能在本类中使用, 外边都不能用
        # __filter_container__: 内置魔法方法, 只能在本类中使用, 外边都不能用
        self._filter_container =  set()

    def add_fp(self, fp):
        # 添加指纹到set集合中
        self._filter_container.add(fp)

    def exists(self, fp):
        """判断指纹是否存在"""
        if fp in self._filter_container:
            return True
        else:
            return False

from ..conf.settings import REDIS_SET_NAME, REDIS_HOST, REDIS_PORT, REDIS_DB
import redis

class RedisFilterContainer(BasicFilterContainer):

    def __init__(self, name=REDIS_SET_NAME, host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB):
        # 建立Redis数据库连接
        self.__server = redis.StrictRedis(host=host, port=port, db=db)
        # set集合在redis中的key
        self.name = name

    def add_fp(self, fp):
        """把指纹添加到Redis的set集合中"""
        self.__server.sadd(self.name, fp)

    def exists(self, fp):
        """判断是否存储"""
        return self.__server.sismember(self.name, fp)

    def clear(self):
        """清空指纹数据"""
        self.__server.delete(self.name)

