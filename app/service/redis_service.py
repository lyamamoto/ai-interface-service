from dotenv import load_dotenv
import hashlib
import os
import redis

load_dotenv()

class RedisService:
    def __init__(self, name: str):
        m = hashlib.md5()
        m.update(name.encode('utf-8'))
        self.__hash = m.hexdigest()
        self.__redis = redis.StrictRedis(host=os.getenv("redis.host"), port=os.getenv("redis.port"), decode_responses=True)

    def __parse_key(self, key: str):
        return f"{self.__hash}_{key}_{self.__hash}"

    def set(self, key: str, value: any):
        return self.__redis.set(self.__parse_key(key), value)

    def get(self, key: str):
        return self.__redis.get(self.__parse_key(key))