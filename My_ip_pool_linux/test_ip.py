import gevent.monkey
gevent.monkey.patch_all()
from gevent.pool import Pool
import requests
from random import choice
from queue import Queue
import time
import datetime

from RedisClient import RedisClient
from ip_website import UserAgent_list,test_http_list,test_https_list


class Tester(object):

    def __init__(self):
        self.redis = RedisClient()
        self.queue = Queue()
        self.pool = Pool(5)
        self.is_running = True
        self.num = 0

    def put_proxy(self):
        # 获取所有redis中数据
        test_proxies = self.redis.all('http')
        test_proxies.extend(self.redis.all('https'))
        for proxy in test_proxies:
            self.queue.put(proxy)
            self.num += 1


    def test_conn(self):
        proxy = self.queue.get()
        print("正在测试代理ip：", proxy)
        # 判断协议类型,构建请求头
        type = proxy.split(":")[0]
        if type == "http":
            proxies = {"http": proxy}
            test_url = choice(test_http_list)
        else:
            proxies = {"https": proxy}
            test_url = choice(test_https_list)
        # 连接测试
        try:
            response = requests.get(test_url, proxies=proxies, headers=self.get_headers(), timeout=4)

            if response.status_code == 200:
                self.redis.max(type,proxy)
                print("测试"+ proxy +"通过")
            else:
                print("测试"+ proxy +"的响应状态码有问题：", response.status_code)
                self.redis.decrease(type,proxy)
        except Exception as e:
            print("测试"+ proxy +"的请求发生错误：",e)
            self.redis.decrease(type,proxy)
        self.num -= 1

    def _callback(self,temp):
        if self.is_running:
            self.pool.apply_async(self.test_conn, callback=self._callback)

    def get_headers(self):
        return {
            "User-Agent":choice(UserAgent_list)
        }

    def run(self):
        print("开始测试代理ip池")
        count = self.redis.count('http')
        counts = self.redis.count('https')
        print("当前http剩余", count, "个代理")
        print("当前https剩余", counts, "个代理")
        self.put_proxy()

        for i in range(4):  # 控制并发
            self.pool.apply_async(self.test_conn, callback=self._callback)

        while True:  # 防止主线程结束
            time.sleep(0.001)  # 避免cpu空转，浪费资源
            if self.num<=0:
                self.is_running = False
                break


if __name__ == '__main__':
    tester = Tester()
    tester.run()
    with open("/home/My_ip_pool_linux/log.txt","a") as f:
        f.write(str(datetime.datetime.now())+"test_ip\n")


