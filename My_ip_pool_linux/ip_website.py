# 代理ip网站
website_list = [
    'http://www.ip3366.net/free/',
    # 'http://www.66ip.cn/areaindex_1/1.html', # 无type类型
    'http://www.goubanjia.com/',
    'https://www.xicidaili.com',
    ]
# 测试IP网站
test_http_list = [
    'http://www.xinhuanet.com/',
    'http://www.tianqi.com/',
    'http://www.people.com.cn/'
]
test_https_list = [
    'https://www.baidu.com/',
    'https://www.qq.com/',
    'https://www.sina.com.cn/',
    'https://www.bilibili.com/',
    'https://music.163.com/',
]
# 多种User Agent
UserAgent_list = [
    # 本机useragent,无需测试
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b9pre) Gecko/20101228 Firefox/4.0b9pre',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
]

if __name__ == '__main__':

    # 测试地址是否有用
    import requests

    test_http_list.extend(test_https_list)
    i = 1
    for UserAgent in UserAgent_list:
        headers = {
                    "User-Agent": UserAgent,
                }
        for url in test_http_list:
            resp = requests.get(url,headers=headers)
            print(i,resp.status_code)
            i+=1
