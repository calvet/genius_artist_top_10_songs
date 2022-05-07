import os
from redis import Redis


class RedisCache:
    def __init__(self):
        self.client = Redis(
            host=os.getenv('REDIS_HOST'),
            port=int(os.getenv('REDIS_PORT'))
        )
        self.days_expire = 60 * 60 * 24 * int(os.getenv('REDIS_DAYS_EXPIRE'))

    def get_artist(self, artist_name):
        try:
            if self.client.exists(artist_name):
                return self.client.get(artist_name)
        except Exception as e:
            print(e)

        return None

    def set_artist(self, artist_name, artist_data):
        try:
            if self.client.exists(artist_name):
                self.client.delete(artist_name)

            self.client.set(artist_name, str(artist_data))

            self.client.expire(artist_name, self.days_expire)
        except Exception as e:
            print(e)
