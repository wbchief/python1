'''
获取模块
'''
from urllib import parse

import requests
import time
from pyquery import PyQuery as pq

class CrawerMetaclass(type):
    def __new__(cls, name, bases, attrs):
        '''

        :param name: 类的名称
        :param bases: 父类
        :param atrs: 类中的方法
        :return:
        '''
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)



class Crawer(object, metaclass=CrawerMetaclass):

    def get_proxies(self, callback):
        '''
        以列表形式获取每个方法获取的代理
        :param callback:
        :return:
        '''
        proxies = []
        for proxy in eval('self.{}(10)'.format(callback)):
            print('成功获取代理', proxy)
            proxies.append(proxy)
        return proxies

    def get_page(self, url, headers):
        '''
        获取html
        :param url: 网址
        :return: html
        '''
        try:
            response = requests.get(url, headers=headers)
            #print(response.status_code)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            print(e.args)
            time.sleep(1)
            self.get_page(url, headers)

    def crawl_proxy66(self, page_count=4):
        '''
        代理66 http://www.66ip.cn/2.html
        :param page_count: 页数
        :return: 代理
        '''
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        base_url = 'http://www.66ip.cn/{}.html'
        urls = [base_url.format(i) for i in range(1, page_count+1)]
        for url in urls:
            print('crawing', url)
            html = self.get_page(url, headers)
            #print(html)
            doc = pq(html)
            trs = doc.find('.containerbox table tr:gt(0)').items()
            for tr in trs:
                ip = tr.find('td:nth-child(1)').text()
                port = tr.find('td:nth-child(2)').text()
                #print('代理', ':'.join([ip, port]))
                yield ':'.join([ip, port])

    def crawl_swei360(self, page_count=4):
        '''
        360代理 http://www.swei360.com/?page=
        :param page_count:  页数
        :return: 代理
        '''
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        base_url = 'http://www.swei360.com/?'
        urls = [base_url + parse.urlencode({'page': i}) for i in range(1, page_count+1)]
        for url in urls:
            print('crawing', url)
            html = self.get_page(url, headers)
            doc = pq(html)
            trs = doc.find('#list > table > tbody > tr').items()
            for tr in trs:
                ip = tr.find('td:nth-child(1)').text()
                port = tr.find('td:nth-child(2)').text()
                #print('代理', ':'.join([ip, port]))
                yield ':'.join([ip, port])

    def crawl_kuaidauli(self, page_count=4):
        '''
        获取快代理 https://www.kuaidaili.com/free/inha/2/
        :param page_count: 页数
        :return: 代理
        '''
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        base_url = 'https://www.kuaidaili.com/free/inha/{}'
        urls = [base_url.format(i) for i in range(1, page_count+1)]
        for url in urls:
            print('crawing', url)
            html = self.get_page(url, headers)
            doc = pq(html)
            trs = doc.find('#list > table > tbody > tr').items()
            for tr in trs:
                ip = tr.find('td:nth-child(1)').text()
                port = tr.find('td:nth-child(2)').text()
                #print('代理', ':'.join([ip, port]))
                yield ':'.join([ip, port])


if __name__ == '__main__':
    crawer = Crawer()
    #crawer.crawl_proxy66()
    #crawer.crawl_swei360()
    crawer.crawl_kuaidauli()