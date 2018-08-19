# _*_ coding:utf-8 _*_

"""
封装爬虫提取出来的数据的
- 将来可以根据这个类型来判断爬虫提取是数据还是请求

"""


class Item(object):

    def __init__(self, data):
        # 设置为私有属性, 为了保护Item中封装的数据
        self._data = data

    @property
    def data(self):
        # 返回真实封装数据
        return self._data