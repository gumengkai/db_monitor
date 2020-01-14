# encoding:utf-8
import redis

class RedisBase(object):
    def __init__(self,params):
        self.params = params
        self.host = self.params['host']
        self.port = self.params['port']
        self.password = self.params['password']

    @classmethod
    def convert_params(cls,params):
        params['port'] = int(params.get('port', 0))
        return params

    def connection(self):
        self.params = self.convert_params(self.params)
        try:
            redis_conn = redis.StrictRedis(host=self.host, port=self.port, password=self.password)
            return redis_conn
        except Exception as e:
            print('redis connect error:{}'.format(e))


