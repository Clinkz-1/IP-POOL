import time
import datetime

from RedisClient import RedisClient
from spider1 import Spider1
from spider3 import Spider3

class Getter(object):

    def __init__(self):
        self.redis = RedisClient()
        self.spider1 = Spider1()
        self.spider3 = Spider3()

    def get_ips_list(self):
        try:
            ips_list = []
            ips_list.extend(self.spider1.run())
            time.sleep(0.5)
            ips_list.extend(self.spider3.run())
        except Exception as e:
            print(e)
            self.get_ips_list()
        else:
            return ips_list

    def run(self):
        print('开始抓取代理IP')
        ips_list = self.get_ips_list()
        ips_temp = []
        for ip in ips_list:
            # 过滤重复数据
            if ip in ips_temp:
                continue
            if ip.split(":")[0] == "http":
                self.redis.add('http',ip)
            else :
                self.redis.add('https',ip)
            ips_temp.append(ip)
        print("抓取代理ip结束")

if __name__ == '__main__':
    getter = Getter()
    getter.run()
    with open("/home/My_ip_pool_linux/log.txt","a") as f:
        f.write(str(datetime.datetime.now())+"get_ip\n")
