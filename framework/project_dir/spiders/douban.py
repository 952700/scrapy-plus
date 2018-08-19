"""项目中的爬虫"""
from scrapy_plus.core.spider import Spider
from scrapy_plus.items import Item
from scrapy_plus.http.request import Request

# 2.0.1-1: 项目中定义爬虫, 传入到框架中, 定义爬虫
class DoubanSpider(Spider):
    # 2.3.3: 增加name属性
    name = 'douban'

    start_urls = ['https://movie.douban.com/top250']

    headers = {
        'Cookie': 'll="118281"; bid=paiNMI3mWpw; _vwo_uuid_v2=DF81AC743E475169D55646C8AD0B343C1|060c18453ea39b3a3d2fba860d4a4502; __yadk_uid=Vj9rD5LSB5bP0RfMXCTCpsZkRQ7PdDNY; _ga=GA1.2.139295724.1526528705; ap=1; ct=y; douban-fav-remind=1; ps=y; ue="583349285@qq.com"; dbcl2="177330829:o59ll0/S1WA"; ck=NiYF; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1533784311%2C%22https%3A%2F%2Fwww.douban.com%2Faccounts%2Flogin%3Fredir%3Dhttps%253A%252F%252Fmovie.douban.com%252F%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.139295724.1526528705.1533690644.1533784311.7; __utmb=30149280.0.10.1533784311; __utmc=30149280; __utmz=30149280.1533784311.7.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; __utma=223695111.139295724.1526528705.1533690644.1533784311.6; __utmb=223695111.0.10.1533784311; __utmc=223695111; __utmz=223695111.1533784311.6.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; _pk_id.100001.4cf6=3c7a5e52db8f3592.1533170858.6.1533784320.1533693222.'
    }

    def start_requests(self):

        for start_url in self.start_urls:

            yield Request(start_url, headers=self.headers)

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
            yield Request(data['movie_url'], callback=self.parse_detail, meta={'data': data}, headers=self.headers)

    def parse_detail(self, response):
        # 获取上一个解析函数传递过来的数据
        data = response.meta['data']
        data['movie_length'] = response.xpath('//span[@property="v:runtime"]/text()')
        # 返回结果
        return Item(data)

