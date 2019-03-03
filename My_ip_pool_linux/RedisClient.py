from random import choice
import redis

from error import PoolEmptyError
from settings import *


class RedisClient():
    def __init__(self,host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化Redis,默认地址,端口号,密码
        """
        self.db = redis.StrictRedis(host=host, port=port,password=password,decode_responses=True)

    def add(self,redis_key,proxy,score=DEFAULT_SCORE ):
        """
        保存代理IP到redis
        :param proxy: 代理IP地址
        :param score: 保存时的分数
        :return: 1:保存成功 0:保存失败
        """
        if not self.db.zscore(redis_key,proxy):
            return  self.db.zadd(redis_key,{ proxy:score })

    def random_get(self,redis_key):
        """
        获取随机的有效IP
        """
        result = self.db.zrangebyscore(redis_key, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(redis_key, 0, 60)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self,redis_key ,proxy):
        """
        代理分数 -1 分, 小于最小值则删除
        """
        score = self.db.zscore(redis_key, proxy)
        if score and score > MIN_SCORE:
            print("代理IP：", proxy, "分数减1,还剩 ",score-1)
            return self.db.zincrby(redis_key,-1 , proxy)
        else:
            print("代理IP：", proxy, "已移除")
            return self.db.zrem(redis_key, proxy)

    def exists(self,redis_key, proxy):
        """
        判断代理ip是否存在,存在True,不在False
        """
        score = self.db.zscore(redis_key, proxy)
        if score<=0 or score == None:
            return False
        return True

    def max(self,redis_key, proxy):
        """
        将代理设置为MAX_SCORE
        """
        return self.db.zadd(redis_key,{ proxy:MAX_SCORE })

    def count(self,redis_key):
        """
        获取代理的数量
        """
        return self.db.zcard(redis_key)

    def all(self,redis_key):
        """
        获取全部代理
        :return: 全部代理的列表
        """
        return self.db.zrangebyscore(redis_key, MIN_SCORE, MAX_SCORE)

    def batch(self,redis_key, start, stop):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        return self.db.zrevrange(redis_key, start, stop - 1)

if __name__ == '__main__':
    conn = RedisClient()
