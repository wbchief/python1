'''
存储模块
'''

from random import choice

from python3.proxies.error import PoolEmptyError
from python3.proxies.setting import *
import redis

class Store:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        '''
        初始化
        :param host: 主机
        :param port: 端口
        '''
        self.db = redis.StrictRedis(host=host, port=port)

    def add(self, proxy, score= INIT_SCORE):
        '''
        添加代理，设置分数
        :param proxy: 代理
        :param score:  分数
        :return: 添加结果
        '''
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)

    def random(self):
        '''
        获取随机有效代理，首先尝试获取最高分数代理，如果不存在，则按排名获取，否则异常
        :return: 代理
        '''
        result = self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError
    def decrease(self, proxy):
        '''
        代理值减一，分数小于最小值时，移除
        :param proxy: 代理
        :return: 修改后的代理分数
        '''
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减一')
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)
    def exists(self, proxy):
        '''
        判断代理是否存在
        :param proxy:  代理
        :return: 是否存在
        '''
        return not self.db.zscore(REDIS_KEY, proxy) == None
    def max(self, proxy):
        '''
        将代理分数设置最大
        :param proxy:  代理
        :return: 设置结果
        '''
        print('代理', proxy, '可用,设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        '''
        代理数量
        :return: 数量
        '''
        return self.db.zcard(REDIS_KEY)

    def all(self):
        '''
        获取全部代理
        :return: 全部代理列表
        '''
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

if __name__ == '__main__':
    store = Store()
    store.add('12312')
    print(store.all())

