# _*_ coding:utf-8 _*_

"""
封装响应数据的
"""
# 2.2.1-2: 给Request增加解析数据的方法
# 支持: json, 正则find_all, xpath

import json
import re
from lxml import etree # 在这里requirements.txt说明

class Response(object):
    # 2.1.2-3: 增加一个meta参数
    def __init__(self, url, status_code, headers, body=None, encoding='utf8', meta={}):
        self.url = url
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.encoding = encoding
        # 给meta赋值
        self.meta = meta

    def json(self):
        """把响应数据,转换为字典"""
        return json.loads(self.body.decode(self.encoding))

    def re_find_all(self, pattern, content=None):
        """
        使用正则的find_all方法提取数据
        :param pattern: 正则模式字符串
        :param content: 内容字符串
        :return: 匹配的结果
        """
        # 如果content没有数据, 那么就是响应体
        if not content:
            content = self.body.decode(self.encoding)

        # 使用正则解析内容
        return re.findall(pattern, content, re.S)

    def xpath(self, query):
        """
        使用xpath从响应数据中提取内容
        :param query: xpath路径字符串
        :return: xpath提取的出来的结果
        """
        # 把响应数据转换为Element对象, 该对象上就可以使用xpath
        element = etree.HTML(self.body)
        # 使用xpath提取数据
        return element.xpath(query)

