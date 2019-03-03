from random import choice
import time
import redis
db = redis.StrictRedis(host='127.0.0.1',port=6379,decode_responses=True)

# a = db.zscore('proxies',"https://175.11.193.162:811")
# print(a)
# print(db.zadd('proxies', {'b123': 100}))
# print(db.zincrby('proxies',-1,'b123'))
# print(db.zrem('proxies','b123'))
# print(db.zscore('proxies','c123'))
# print(db.zadd('proxies',{'a123':50}))
# print(db.zcard('proxies'))
# print(db.zrevrange('proxies',0,4))
# print(db.zrangebyscore('proxies',0,100))



