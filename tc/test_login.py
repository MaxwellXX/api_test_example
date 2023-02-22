#coding:utf-8
import pytest
import json
import logging
from com.log import Logger
from com.mhttp import Request
from com.config import Config
from com.util import read_yaml
from com.assertion import BaseAssertion, ExtendAssertion
from datetime import datetime
from com.util import decrype

request = Request()
log = Logger(__name__, CmdLevel=logging.INFO, FileLevel=logging.INFO)
c = Config()

test_data = read_yaml('data/login_para.yaml')
test_steps = [data.get('step') for data in test_data]
index = 0

@pytest.mark.parametrize('datas', test_data, ids=test_steps)
def test_login_ok(datas):
    global index
    log.logger.info('--------------testing id: "{}", step: "{}"-----------'.format(index, test_steps[index]))
    url = c.get_env()['host'] + datas['url']
    log.logger.info('testing api: {}'.format(url))

    r = request.post(url, headers={'Content-Type': 'application/json'},
                     data=json.dumps(datas['data']), verify=False)

    index = index + 1

    if r.status_code < 500:
        body = r.json()

        base = BaseAssertion(body)
        log.logger.info('doing base assertion, assert status code OK ')
        assert base.status_code_ok(r.status_code) or base.auth_error(r.status_code)

        if not datas.get('base_assertion_only'):
            extended = ExtendAssertion(body)
            for e in datas.get('expect'):
                if e['type'] == 'path_value_equal':
                    log.logger.info('doing extended assertion path_value_equal')
                    for data in e['data']:
                        assert extended.path_value_equal(data.get('keys'), data.get('value'))
                elif e['type'] == 'path_value_greater':
                    log.logger.info('doing extended assertion path_value_greater')
                    for data in e['data']:
                        assert extended.path_value_greater(data.get('keys'), data.get('value'))
                elif e['type'] == 'keys_equal':
                    log.logger.info('doing extended assertion keys_equal ')
                    for data in e['data']:
                        assert extended.keys_equal(data.get('keys'), data.get('value'))
                elif e['type'] == 'keys_partial':
                    log.logger.info('doing extended assertion keys_partial ')
                    for data in e['data']:
                        assert extended.keys_partial(data.get('keys'), data.get('value'))
    else:
        log.logger.info('api call fails, code: {}, message: {}'.format(r.status_code, r.json()))
        pytest.fail('current api call fails, please see log for details!')

    log.logger.info('finished testing id: "{}", step: "{}"'.format(index - 1, test_steps[index - 1]))
    log.logger.info('-------------------------------END TEST---------------------------------------')


if __name__ == '__main__':
    print('s' in ['s', 'p'])
    pytest.main(["-s","test_login.py"])
