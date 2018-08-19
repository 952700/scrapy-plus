# _*_ coding:utf-8 _*_

"""
下载器中间件:
用于处理请求和响应


"""

class BaiduDownloaderMiddleware(object):

    def process_request(self, request):
        # 处理请求
        print("BaiduDownloaderMiddleware: process_request")
        return request

    def process_response(self, response):
        # 处理请求
        print("BaiduDownloaderMiddleware: process_response")
        return response


class DoubanDownloaderMiddleware(object):

    def process_request(self, request):
        # 处理请求
        print("DoubanDownloaderMiddleware: process_request")
        return request

    def process_response(self, response):
        # 处理请求
        print("DoubanDownloaderMiddleware: process_response")
        return response