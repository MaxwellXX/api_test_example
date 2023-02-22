# coding:utf-8
import pytest
import json
import logging
import traceback
import sys
from jsonschema import validate, SchemaError, ValidationError
from com.log import Logger
from com.mhttp import Request
from com.config import Config
from com.util import get_common_header
from com.util import decrype
from com.util import load_json
from com.util import read_yaml

request = Request()
log = Logger(__name__, CmdLevel=logging.INFO, FileLevel=logging.INFO)
c = Config()
test_data = read_yaml('data/api_spl.yaml')
path = '/api_spl/_search'
url = c.get_env()['host'] + path

@pytest.mark.parametrize('datas', test_data)
def test_api_with_different_user(datas):
    log.logger.info('--------------testing step: "{}"-----------'.format(datas['step']))
    # log.logger.info('url: {}'.format(url))
    debug = c.get_config('DEFAULT', 'DEBUG')

    r = request.post(c.get_env()['host'] + '/login',
                     headers={'Content-Type': 'application/json'},
                     data=json.dumps({"username": datas['username'], "password": datas['pwd']}),
                     verify=False)
    # log.logger.info('login response: {}'.format(r))
    apikey = r.json()['token']
    secrets = r.json()['secrets']
    payload = json.loads('{"filter":{"field1":["'+datas['pid']+'"]}}')
    # log.logger.info('api payload: {}'.format(payload))
    response = request.post(url,
                            headers=get_common_header('POST', path, apikey, secrets),  # method should be in upper case
                            data=json.dumps(payload),
                            verify = False
                            )
    # log.logger.info('api response: {}'.format(response))
    if debug == 'False':
        dic = json.loads(decrype(response))
        # log.logger.info('api response detail: {}'.format(dic))
    else:
        dic = json.loads(response)

    expect_skus_set = set(datas['permission_brand'])
    real_skus_set = set()
    xxx_api_schema = load_json('data/schema/api_schema_xxx_kpi.json')
    own_api_spl_schema = load_json('data/schema/api_spl_own_schema.json')

    try:
        # print(dic['hits']['hits'])
        xxx_api = dic['hits']['hits'][0]['_source']['api_spl'].replace("\\", "")
        log.logger.info('xxx_api detail: {}'.format(xxx_api))
        # print(xxx_api)
        own_api = dic['own_api_spl'][datas['pid']]
        avlength = len(own_api)
        store_count = 0

        for x in own_api:
            real_skus_set.add(x['brand'])
            store_count += x['store_count']

        # print(own_api_spl_schema)
        # print(own_api)
        xxx_api_schema_check = True if validate(json.loads(xxx_api),xxx_api_schema) is None else False
        own_api_spl_schema_check = True if validate(own_api,own_api_spl_schema) is None else False

        assert xxx_api_schema_check is True
        log.logger.info('assert validate(xxx_api,xxx_api_schema_check) is None, result: {}'.format(
            xxx_api_schema_check))

        assert own_api_spl_schema_check is True
        log.logger.info('assert validate(own_api,own_api_spl_schema) is None, result: {}'.format(own_api_spl_schema_check))

        assert avlength == datas['avlength']
        log.logger.info('assert user can see {} actual and virtual stores in total, result: {}'.format(datas['avlength'],avlength == datas['avlength']))

        assert store_count == datas['store_count']
        log.logger.info('assert user can see {} actual stores, result: {}'.format(datas['store_count'], avlength == datas['store_count']))

        assert set(expect_skus_set).issuperset(real_skus_set)
        log.logger.info('assert own_api_spl store sku can only be children of permission sku, result: {}'.format(set(expect_skus_set).issuperset(real_skus_set)))
    except KeyError as e:
        log.logger.info('[own_api_spl][pid] keyerror')
        pytest.fail('[own_api_spl][pid] keyerror mark as fail, please see log for details!')
    except SchemaError as e:
        log.logger.info('xxx_api or own_api_spl SchemaError ')
        pytest.fail('xxx_api or own_api_spl SchemaError, please see log for details!')
    except ValidationError as e:
        log.logger.info('xxx_api or own_api_spl ValidationError')
        pytest.fail('xxx_api or own_api_spl ValidationError, please see log for details!')


