# _*_ coding:utf-8 _*_

"""
管道模块
1. 处理数据的
"""

class Pipeline(object):

    def process_item(self, item):
        # 处理爬虫提取出来的数据
        print(item.data)

        return item