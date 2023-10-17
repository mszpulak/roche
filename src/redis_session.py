import os
import pickle
from functools import wraps
from typing import Any

from dotenv import load_dotenv
from redis.asyncio.cluster import RedisCluster as ARedisCluster
from redis.cluster import RedisCluster

from src.logger import server_logger

load_dotenv()
REDIS_SERVER = os.getenv("REDIS_SERVER")
REDIS_PASS = os.getenv("REDIS_PASS")


async def aget_redis_client():
    server_logger.info("RedisCluster:" + REDIS_SERVER)
    client = ARedisCluster(host=REDIS_SERVER, password=REDIS_PASS)
    await client.initialize()
    server_logger.info("Ping successful" + str(await client.ping()))
    yield client
    await client.aclose()


def get_redis_client():
    server_logger.info("RedisCluster:" + REDIS_SERVER)
    client = RedisCluster(host=REDIS_SERVER, password=REDIS_PASS)
    server_logger.info("Ping successful" + str(client.ping()))
    yield client
    client.close()


class Cacher:
    signature = "state_machine_id"

    def __init__(self, redis_client):
        self.redis_client = redis_client

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = self.redis_load()
            if result is None:
                result = func(*args, **kwargs)
                self.redis_dump(result)
            return result

        return wrapper

    def redis_dump(self, m: Any) -> None:
        dump = pickle.dumps(m)
        self.redis_client.set(self.signature, dump)

    def redis_load(self) -> Any:
        m = self.redis_client.get(self.signature)
        if m:
            m = pickle.loads(m)
        return m

    async def aredis_dump(self, m: Any) -> None:
        dump = pickle.dumps(m)
        await self.redis_client.set(self.signature, dump)

    async def aredis_load(self) -> Any:
        m = await self.redis_client.get(self.signature)
        if m:
            m = pickle.loads(m)
        return m
