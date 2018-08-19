DEFAULT_LOG_FILENAME = 'itcast.log'


# 2.5-1 能够在settings文件中配置,开启哪些爬虫,管道, 下载中间件爬虫中间件

# 爬虫
SPIDERS = [
    # 'spiders.sina.SinaSpider',
    'spiders.baidu.BaiduSpider',
    'spiders.douban.DoubanSpider'
]

PIPELINES = [
    'pipelines.BaiduPipeline',
    'pipelines.DoubanPipeline',
]

# DOWNLOADER_MIDDLEWARES = [
#     'middlewares.downloader_middlewares.BaiduDownloaderMiddleware',
#     'middlewares.downloader_middlewares.DoubanDownloaderMiddleware',
# ]
#
# SPIDER_MIDDLEWARES = [
#     'middlewares.spider_middlewares.BaiduSpiderMiddleware',
#     'middlewares.spider_middlewares.DoubanSpiderMiddleware',
# ]

# 异步个数
ASYNC_COUNT = 2

# 3.1-1 异步类型: thread(线程), coroutine(协程)
ASYNC_TYPE = 'coroutine'

# 开启分布式: 实现调度数据持久化
SCHEDULE_PERSIST = True

# 设置关闭断点续爬, 默认开启的
# FP_PERSIST = False