from scrapy_plus.core.engine import Engine

if __name__ == '__main__':
    # 2.5: 通过配置文件动态设置爬虫,管道, 中间件后
    # 创建引擎对象
    engine = Engine()

    # 启动引擎
    engine.start()
