from flask import Flask, g, redirect, url_for, request
from RedisClient import RedisClient
from api_test_ip import Tester
import requests
import time

app = Flask(__name__)

def get_conn():
    if not hasattr(g, "redis"):
        g.redis = RedisClient()
    return g.redis


@app.route("/")
def index():
    html_str = """<h1 style='text-align:center'>欢迎使用个人代理IP池</h1>
    <br>
    <br>
    <p style='text-align:center'> 
    请求方式(GET):<br>
    /get  获取1条http代理ip<br>
    /gets  获取1条https代理ip<br>
    /get/(1-10)  获取(1-10)条http代理ip<br>
    /gets/(1-10) 获取(1-10)条https代理ip<br>
    /count 查看代理ip数量<br>
    自动测试(POST):<br>
    /testip  请求体中带上目标url,等待3分钟<br>
    /getip  请求体中带上目标url,获取代理ip<br>
    eg:请求体就带上"https://www.baidu.com"<br>
    by:cjn,lxy<br>
    </p>
    """
    return html_str

@app.route("/get")
def get_proxy():
    """
    获取随机代理的接口
    :return: 随机代理ip
    """
    return redirect(url_for('get_proxies',num=1))

@app.route("/get/<int:num>")
def get_proxies(num):
    """
    获取随机代理的接口
    :return: 随机代理ip
    """
    coon = get_conn()
    if num<=1:
        return coon.random_get('http')
    ip_more = ''
    num = num if num < 10 else 10
    for i in range(num):
        ip_more+=coon.random_get('http')+' '
    return ip_more[:-1]

@app.route("/count")
def get_conuts():
    """
    获取代理ip池总量
    :return: 总数量
    """
    coon = get_conn()
    str = """
    http代理有{}个 , https代理有{}个
    """.format(coon.count('http'),coon.count('https'))
    return str

@app.route("/gets")
def gets_proxy():
    """
    获取随机代理的接口
    :return: 随机代理ip
    """
    return redirect(url_for('gets_proxies',num=1))

@app.route("/gets/<int:num>")
def gets_proxies(num):
    """
    获取随机代理的接口
    :return: 随机代理ip
    """
    coon = get_conn()
    if num<=1:
        return coon.random_get('https')
    ip_more = ''
    num = num if num < 10 else 10
    for i in range(num):
        ip_more+=coon.random_get('https')+' '
    return ip_more[:-1]

@app.route("/testip",methods=['POST'])
def test_ip():
    """
    post请求测试特定url
    :return: 格式是否符合
    """
    url = request.data.decode()

    # https://weibo.cn
    try:
        requests.get(url)
    except Exception :
        return "该url格式出错或无法访问"
    type = url.split(':')[0]
    temp_time = time.time()
    test = Tester(type,url)
    test.run()
    return "测试结束,用时%0.2f秒"%(time.time()-temp_time)

@app.route("/getip",methods=['POST'])
def get_test_ip():
    """
    post请求获取特定url
    :return: 测试的结果
    """
    url = request.data.decode()
    try:
        requests.get(url)
    except Exception :
        return "该url格式出错或无法访问"
    coon = get_conn()
    count = coon.count(url)
    if count == 0 :
        return "该url尚未测试"
    else:
        ip_more = ''
        for ip in coon.all(url):
            ip_more += ip + ' '
        return ip_more[:-1]


if __name__ == '__main__':
    app.run(threaded = True)
