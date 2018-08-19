"""项目中的爬虫"""
from scrapy_plus.core.spider import Spider
from scrapy_plus.items import Item
from scrapy_plus.http.request import Request

# 2.0.1-1: 项目中定义爬虫, 传入到框架中, 定义爬虫

class BaiduSpider(Spider):
    # 2.0.2-1: 定义起始URL列表
    start_urls = ['http://www.baidu.com', 'http://www.itcast.cn']


class DoubanSpider(Spider):

    start_urls = ['https://movie.douban.com/top250']

    # 2.1.2-1: 解析函数返回多个数据
    def parse(self, response):
        # 提取a标签的列表
        a_s = response.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a')
        for a in a_s:
            data = {}
            data['movie_name'] = a.xpath('./span[1]/text()')[0]
            data['movie_url'] = a.xpath('./@href')[0]
            # yield Item(data)

            #2.1.2-1: 构建详情页的请求交给引擎
            yield Request(data['movie_url'], callback=self.parse_detail, meta={'data': data})

    def parse_detail(self, response):
        # 获取上一个解析函数传递过来的数据
        data = response.meta['data']
        data['movie_length'] = response.xpath('//span[@property="v:runtime"]/text()')
        # 返回结果
        return Item(data)

