# _*_ coding:utf-8 _*_

"""
下载器中间件:
用于处理请求和响应

2.4-1: 创建middlwares文件夹, 下面创建两个文件分别是downloader_middlewares.py,spider_middlewares.py
downloader_middlewares.py
    - 定义两个下载器中间件

spider_middlewares.py
    - 定义两个爬虫中间件
"""

class DownloaderMiddleware(object):

    def process_request(self, request):
        # 处理请求
        print("DownloaderMiddleware: process_request")
        return request

    def process_response(self, response):
        # 处理请求
        print("DownloaderMiddleware: process_response")
        return response