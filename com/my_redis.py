try:
    import redis
except ImportError:
    # We can allow custom provider only usage without redis-py being installed
    redis = None
from com.config import Config
import logging
from com.log import Logger

c = Config()
log = Logger(__name__, CmdLevel=logging.INFO, FileLevel=logging.INFO)


class Redi(object):

    def __init__(self):
        debug = c.get_config('DEFAULT', 'DEBUG')
        redis_url = None
        if debug == 'True':
            redis_url = c.get_config('REDIS', 'DEBUG_URL')
        else:
            redis_url = c.get_config('REDIS', 'URL')
        log.logger.info('connecting to redis: "{}"'.format(redis_url))
        self._redis_client = redis.from_url(redis_url)

    def __getattr__(self, name):
        return getattr(self._redis_client, name)

    def __getitem__(self, name):
        return self._redis_client[name]

    def __setitem__(self, name, value):
        self._redis_client[name] = value

    def __delitem__(self, name):
        del self._redis_client[name]