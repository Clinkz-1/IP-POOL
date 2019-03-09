import requests
from lxml import etree
from RedisClient import RedisClient

class Spider1(object):

    def __init__(self):
        self.start_url = "http://www.ip3366.net/free/?stype={}&page={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        self.redis = RedisClient()
        self.coon_num = 0

    def get_proxies(self):
        try :
            return {'http':self.redis.random_get('http')}
        except Exception as e:
            print(e)
            return None

    def get_url_list(self):
        url_list = []
        url_list.extend([self.start_url.format(1,i) for i in range(1,5)])
        url_list.extend([self.start_url.format(3,i) for i in range(1,3)])
        return url_list

    def get_page_data(self, url):
        try:
            response = requests.get(url,headers = self.headers,proxies =self.get_proxies(),timeout=5)
            return response.content
        except Exception as e:
            self.coon_num+=1
            if self.coon_num >=3:
                return requests.get(url,headers = self.headers).content
            print(e)
            return self.get_page_data(url)

    def get_ip(self, html_str):
        html = etree.HTML(html_str)
        tr_list = html.xpath("//div[@id='list']//tbody/tr")
        ip_list = []
        for tr in tr_list:
            ip = tr.xpath("./td[1]/text()")[0]
            port = tr.xpath("./td[2]/text()")[0]
            type = tr.xpath("./td[4]/text()")[0]
            speed = tr.xpath("./td[6]/text()")[0]
            if int(speed[0])>3:
                continue
            url = type.lower() + "://" + ":".join([ip, port])
            if url in ip_list:
                continue
            ip_list.append(url)
        return ip_list

    def run(self):
        # 1. url_list
        url_list = self.get_url_list()
        ips_list = []
        # 2. 发送请求  获取响应
        for url in url_list:
            html_str = self.get_page_data(url)
            self.coon_num = 0
            # 3. 提取数据
            ip_list = self.get_ip(html_str)
            ips_list.extend(ip_list)
        return ips_list


if __name__ == '__main__':
    spider1 = Spider1()
    print(len(spider1.run()))
