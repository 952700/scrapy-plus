from scrapy_plus.core.engine import Engine
from spiders.baidu import BaiduSpider
from spiders.douban import DoubanSpider

from pipelines import BaiduPipeline,DoubanPipeline
from middlewares.downloader_middlewares import  BaiduDownloaderMiddleware
from middlewares.downloader_middlewares import  DoubanDownloaderMiddleware

from middlewares.spider_middlewares import BaiduSpiderMiddleware
from middlewares.spider_middlewares import DoubanSpiderMiddleware

if __name__ == '__main__':

    # 创建百度爬虫
    baidu_spider = BaiduSpider()
    # 2.1.1-3:  创建豆瓣爬虫
    douban_spider = DoubanSpider()
    #2.2-1 准备一个爬虫字典
    # 2.3.5: 把原来写死的名称, 换成为爬虫中的名称
    spiders = {
        BaiduSpider.name: baidu_spider,
        DoubanSpider.name: douban_spider
    }
    # # 2.3-6: 创建管道列表, 传入到引擎中
    pipelines = [BaiduPipeline(), DoubanPipeline()]

    # 2.4-2: 定义爬虫中间列表和下载器中间件列表
    spider_middlewares = [
        BaiduSpiderMiddleware(),
        DoubanSpiderMiddleware(),
    ]

    downloader_middlewares = [
        BaiduDownloaderMiddleware(),
        DoubanDownloaderMiddleware()
    ]
    # 2.4.3: 把爬虫中间列表和下载器中间件列表传入给引擎
    # 创建引擎对象
    engine = Engine(spiders, pipelines, spider_middlewares, downloader_middlewares)

    # 启动引擎
    engine.start()
