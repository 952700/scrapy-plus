from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request
from scrapy_plus.items import Item
import time

class SinaSpider(Spider):

    name = 'sina'

    def start_requests(self):

        url = 'http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php'

        while True:

            yield Request(url, dont_filter=True)
            # 一定要等待一定要再yield后面, 否则会导致程序卡死了
            time.sleep(10)

    def parse(self, response):
        # 设置编码方式为GBK
        # response.encoding = 'GBK'
        # result = response.re_find_all('{channel\s*:\s*{title\s*:\s*"(.+?)",')
        print(response.url)

        return Item(response.url)



