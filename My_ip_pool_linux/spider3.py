import requests
from lxml import etree
from RedisClient import RedisClient

class Spider3(object):

    def __init__(self):
        self.start_url = "https://www.xicidaili.com/nn/{}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        self.redis = RedisClient()
        self.coon_num = 0

    def get_proxies(self):
        try :
            return {'https': self.redis.random_get('https')}
        except Exception as e:
            print(e)
            return None

    def get_url_list(self):
        url_list = [self.start_url.format(i) for i in range(1,3)]
        return url_list

    def get_page_data(self, url):
        try:
            response = requests.get(url,headers = self.headers,proxies =self.get_proxies(),timeout=5)
            return response.content
        except Exception as e:
            self.coon_num += 1
            if self.coon_num >= 3:
                return requests.get(url, headers=self.headers).content
            print(e)
            return self.get_page_data(url)

    def get_ip(self, html_str):
        html = etree.HTML(html_str)
        tr_list = html.xpath("//table[@id='ip_list']/tr")[1:]
        ip_list = []
        for tr in tr_list:
            ip = tr.xpath("./td[2]/text()")[0]
            port = tr.xpath("./td[3]/text()")[0]
            type = tr.xpath("./td[6]/text()")[0]
            speed = tr.xpath("./td[7]/div/@title")[0][:-1]
            if float(speed)>5:
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
            self.get_ip(html_str)
            ip_list = self.get_ip(html_str)
            ips_list.extend(ip_list)
        return ips_list


if __name__ == '__main__':
    spider3 = Spider3()
    print(len(spider3.run()))


