python3 set_time.py
cron test_ip.cron
cron get_ip.cron
gunicorn -w 2 -b 127.0.0.1:5000 flask:app
