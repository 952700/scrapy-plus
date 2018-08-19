# _*_ coding:utf-8 _*_

"""
封装请求数据的
"""


class Request(object):
    #2.1.2-2: 支持callback和meta参数
    # 3.3.1-1: 能够支持重复请求的配置, 不过滤
    def __init__(self, url, method="GET", headers={}, params={}, data={}, cookies={}, callback=None, meta={}, dont_filter=False):
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.cookies = cookies

        self.callback = callback
        self.meta = meta

        # 记录是否需要过滤
        self.dont_filter = dont_filter
