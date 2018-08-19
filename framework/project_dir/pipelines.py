
# 2.3-1: 实现百度和豆瓣的pipeline

class BaiduPipeline(object):

    def process_item(self, item, spider):
        if spider.name == 'baidu':
            print("百度爬虫数据: {}".format(item.data))

        return item


class DoubanPipeline(object):

    def process_item(self, item, spider):
        if spider.name == 'douban':
            print("豆瓣爬虫数据: {}".format(item.data))

        return item