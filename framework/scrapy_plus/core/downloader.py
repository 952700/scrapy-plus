# _*_ coding:utf-8 _*_

import requests
from ..http.response import Response
"""
下载器模块
1. 请求请求对象, 发送请求或相应数据, 封装为Response对象返回
"""


class Downloader(object):

    def get_response(self, request):
        # 1. 请求请求对象, 发送请求或相应数据, 封装为Response对象返回
        if request.method.upper() == 'GET':
           res = requests.get(request.url, headers=request.headers, params=request.params, cookies=request.cookies)
        elif request.method.upper() == 'POST':
           res = requests.post(request.url, headers=request.headers, data=request.data, cookies=request.cookies)
        else:
            raise Exception("暂时只支持GET和POST请求")

        # 返回封装的后相应数据
        return Response(res.url, res.status_code, res.headers, res.content)