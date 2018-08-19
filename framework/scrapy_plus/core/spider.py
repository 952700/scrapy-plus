# _*_ coding:utf-8 _*_

from ..http.request import Request
from ..items import Item
"""
爬虫模块:
1. 准备起始请求
2. 解析响应数据, 提取数据和请求
"""


class Spider(object):
    # 2.3.2: 增加name属性
    name = 'spider'

    # 2.0.2-2: 修改爬虫模块, 让其支持起始URL列表
    # start_url = "http://www.itcast.cn"
    start_urls = []

    def start_requests(self):
        # 1. 准备起始请求
        # 2.0.2-3: 让其支持起始URL列表
        for start_url in self.start_urls:
            # 使用yield让start_requests方法, 变成一个生成器
            yield Request(start_url)

    def parse(self, response):
        # 2. 解析响应数据, 提取数据和请求

        return Item(response.url)