# _*_ coding:utf-8 _*_

"""
爬虫中间件
"""

class SpiderMiddleware(object):

    def process_request(self, request):
        # 处理请求
        print("SpiderMiddleware: process_request")
        return request

    def process_response(self, response):
        # 处理请求
        print("SpiderMiddleware: process_response")

        return response