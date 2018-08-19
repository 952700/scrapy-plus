from scrapy_plus.core.spider import Spider

# 2.0.1-1: 项目中定义爬虫, 传入到框架中, 定义爬虫

class BaiduSpider(Spider):
    # 2.3.4: 增加name属性
    name = 'baidu'

    # 2.0.2-1: 定义起始URL列表
    start_urls = ['http://www.baidu.com', 'http://www.itcast.cn','http://www.baidu.com','http://www.baidu.com']