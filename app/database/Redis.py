import redis
from config import settings  
from .ConnectionManager import ConnectionManager

class RedisManager(ConnectionManager):
    def __init__(self):
        """
        Open a Redis connection and initialize a client.
        """
        redis_host = settings.REDIS_HOST
        redis_port = settings.REDIS_PORT

        self.client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )

    def get_client(self):
        """
        Returns the Redis client.

        :return: Redis client instance.
        """
        return self.client

    def close_connection(self):
        """
        Close the Redis connection.
        """
        self.client.close()
        print("Redis connection closed.")