from settings import set_get_ip_time,set_test_ip_time


def save(data,file):
    with open('/home/My_ip_pool_linux/'+file,'w') as f:
        f.write(data)

def main():
    get_ip_time = "*/{} * * * * /usr/python3 /home/My_ip_pool_linux/get_ip.py".format(set_get_ip_time)
    test_ip_time = "*/{} * * * * /usr/python3 /home/My_ip_pool_linux/test_ip.py".format(set_test_ip_time)
    save(get_ip_time, 'get_ip.cron')
    save(test_ip_time, 'test_ip.cron')

if __name__ == '__main__':
    main()
