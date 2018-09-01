'''
存储模块 获取器
'''
from python3.proxies.getproxies import Crawer
from python3.proxies.setting import *
from python3.proxies.storeproxy import Store


class Getter():
    def __init__(self):
        self.redis = Store()
        self.crawler = Crawer()

    def is_over_threshold(self):
        '''
        判断是否达到代理池阈值
        :return:
        '''
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print('获取器开始执行')
        if not self.is_over_threshold():
            #print(self.crawler.__CrawlFuncCount__)
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)

if __name__ == '__main__':
    getter = Getter()
    getter.run()