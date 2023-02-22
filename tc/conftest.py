import pytest
import yaml
import logging
import sys
import json
import hashlib
import hmac

from datetime import datetime
from com.log import Logger
from com.config import Config
from com.mhttp import Request
from com.my_redis import Redi

redi = Redi()
log = Logger(__name__, CmdLevel=logging.INFO, FileLevel=logging.INFO)
c = Config()
req = Request()


# before running test, login to set token and secret in redis, so no need to login before every api call
# don't know which way is better, so save to redis anyway
@pytest.fixture(scope="session")
def login():
    login = dict()
    log.logger.info('log into system at the beginning of test, test_user: "{}"'.format(c.get_env()['user']))
    url = c.get_env()['host'] + '/login'
    r = req.post(url,
                 headers={'Content-Type': 'application/json'},
                 data=json.dumps({"username": c.get_env()['user'], "password": c.get_env()['pwd']}),
                 verify=False)
    if r.status_code == 200:
        log.logger.info('the test user log into system successfully! ')
        login['apikey'] = r.json()['token']
        login['secrets'] = r.json()['secrets']
        login['login_time'] = int(datetime.now().timestamp())
        login['id'] = r.json()['id']

        log.logger.info('setting token and secret to redis! ')

        redi.set('apikey', login['apikey'])
        redi.set('secrets', login['secrets'])
        redi.set('login_time', login['login_time'])
        redi.set('id', r.json()['id'])
    else:
        log.logger.log(logging.ERROR, 'Fail to login, exit!')
        sys.exit()

    yield login
    redi.delete('apikey')
    redi.delete('secrets')
    # redi.delete('login_time')
    redi.delete('id')


@pytest.fixture(scope="module")
def get_signature():
    header = {'Content-Type': 'application/json',
              'Accept': 'application/json, text/plain, */*',
              'Authorization': None,
              'LG-Timestamp': None,
              'LG-Content-Sig': None
              }

    def get_hmac(method, url, current_time):
        log.logger.info('setting header for method: {}, api: {} '.format(method, url))
        payload = '{} {} {}'.format(method.upper(), url, current_time)
        signature = hmac.new(redi.get('secrets'), payload.encode('ascii'), digestmod=hashlib.sha256).hexdigest()
        header["Authorization"] = "Bearer " + redi.get('apikey').decode('utf8')
        header["LG-Timestamp"] = current_time
        header["LG-Content-Sig"] = signature
        header["X-disable-encrypt"] = 'true'
        return header

    return get_hmac

# function level by default
# before each api call, we should firstly validate if token and secret exists/expires
# after that, we should get hmac by method, pathname,timestamp,secrets
# at last we should set headers for the api that is being tested
