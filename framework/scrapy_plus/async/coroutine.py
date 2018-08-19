from gevent.pool import Pool as BasicPool
# 打猴子补丁
from gevent import monkey
monkey.patch_all()


"""
实现自己协议池
目的: 让这个协程池和线程池有一样接口
"""


class Pool(BasicPool):

    # 这个方法就和线程池中异步方法完全一样
    def apply_async(self, func, args=(), kwds={}, callback=None, error_callback=None):
        # 调用父类的协程中异步方法
        super().apply_async(func, args=args, kwds=kwds, callback=callback)

    def close(self):
        """增加关闭函数"""
        pass