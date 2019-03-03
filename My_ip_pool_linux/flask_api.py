from flask import Flask, g, redirect, url_for
from RedisClient import RedisClient

app = Flask(__name__)

print()
def get_conn():
    if not hasattr(g, "redis"):
        g.redis = RedisClient()
    return g.redis

@app.route("/")
def index():
    html_str = """<h1 style='text-align:center'>欢迎使用代理IP系统</h1>
    <br>
    <br>
    <p style='text-align:center'> 请求方式:/get  获取1条http代理ip<br>
    /gets  获取1条https代理ip<br>
    /get/(1-10)  获取(1-10)条http代理ip<br>
    /gets/(1-10) 获取(1-10)条https代理ip<br>
    /count 查看代理ip数量<br>
    </p>
            """
    return html_str

@app.route("/get")
def get_proxy():
    """
    获取随机代理的接口
    :return: 随机代理ip
    """
    coon = get_conn()

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
    return ip_more

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
    coon = get_conn()

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
    return ip_more


if __name__ == '__main__':
    app.run(threaded = True)
