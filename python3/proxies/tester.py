'''
检测模块
'''
import asyncio
import aiohttp
import time
try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError

from python3.proxies.setting import *
from python3.proxies.storeproxy import Store


class Testing:

    def __init__(self):
        self.redis = Store()

    async def test_singer_proxy(self, proxy):
        '''
        检测单个代理
        :param proxy: 代理
        :return: None
        '''
        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试', proxy)
                async with session.get(TEST_URL, headers=header, proxy=real_proxy, timeout=1, allow_redirects=False) as response:
                    print(response.status)
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        print('代理可用', proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('请求相应吗不合格', response.status, 'IP', proxy)
            except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError) as e:
                self.redis.decrease(proxy)
                print('代理请求失败', proxy)
                print(e.args)
    def run(self):
        '''
        测试主函数
        :return: None
        '''
        print('测试器开始执行')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            for i in range(0, len(proxies), BATCH_TEST):
                test_proxies = proxies[i: i + BATCH_TEST]
                tasks = [self.test_singer_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(2)
        except Exception as e:
            print('测试器发生错误', e.args)



test = Testing()
test.run()
