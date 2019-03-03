import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}
ip_list = []
ip_list_new=[]
ok = 0
for i in range(2):
    resp = requests.get('http://101.132.131.199/gets/10',headers=headers)
    ip_list.extend(resp.content.decode().strip().split(' '))
for ip in ip_list:
    if ip not in ip_list_new:
        ip_list_new.append(ip)
        proxies = {'https': ip}
        try:
            resp = requests.get('https://www.baidu.com/', headers=headers, proxies=proxies, timeout=4)
        except Exception as e:
            continue
        if resp.status_code and resp.status_code == 200:
            ok += 1

print(len(ip_list_new))
print("ok:",ok)
