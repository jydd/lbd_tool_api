import oss2
from app.config import Config
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from urllib.parse import urlparse, urljoin
from app.extensions import flask_redis
from redis.exceptions import WatchError
from flask import request
import uuid
import time


redis_client = flask_redis


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


#  获取一个分布式锁
def acquire_lock(lock_name, acquire_time=20, time_out=20):
    # 生成唯一id
    identifier = str(uuid.uuid4())
    # 客户端获取锁的结束时间
    end = time.time() + acquire_time
    # key
    lock_names = "lock_name:" + lock_name
    while time.time() < end:
        # setnx(key,value) 只有key不存在情况下，将key的值设置为value，若key存在则不做任何动作,返回True和False
        if redis_client.setnx(lock_names, identifier):
            # 设置键的过期时间，过期自动剔除，释放锁
            redis_client.expire(lock_names, time_out)
            return identifier
        # 当锁未被设置过期时间时，重新设置其过期时间
        elif redis_client.ttl(lock_names) == -1:
            redis_client.expire(lock_names, time_out)
        time.sleep(0.001)

    return False


# 锁的释放
def release_lock(lock_name, identifire):
    lock_names = "lock_name:" + lock_name
    pipe = redis_client.pipeline(True)
    while True:
        try:
            # 通过watch命令监视某个键，当该键未被其他客户端修改值时，事务成功执行。当事务运行过程中，发现该值被其他客户端更新了值，任务失败
            pipe.watch(lock_names)
            print(pipe.get(lock_names))
            if pipe.get(lock_names) == identifire:  # 检查客户端是否仍然持有该锁
                # multi命令用于开启一个事务，它总是返回ok
                # multi执行之后， 客户端可以继续向服务器发送任意多条命令， 这些命令不会立即被执行， 而是被放到一个队列中， 当 EXEC 命令被调用时， 所有队列中的命令才会被执行
                pipe.multi()
                # 删除键，释放锁
                pipe.delete(lock_names)
                # execute命令负责触发并执行事务中的所有命令
                pipe.execute()
                return True
            pipe.unwatch()
            break
        except WatchError:
            # 释放锁期间，有其他客户端改变了键值对，锁释放失败，进行循环
            pass
    return False
