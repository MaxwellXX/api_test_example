import pytest
import logging
import re
from jsonschema import validate, ValidationError
import json
from httmock import all_requests, HTTMock, response
import requests
from com.util import load_json
from com.log import Logger


log = Logger(__name__,CmdLevel=logging.INFO, FileLevel=logging.INFO)


class BaseAssertion(object):
    def __init__(self, res):
        self.res = res

    def find_field(self, res, path):
        if isinstance(res, dict):
            res = [res]
        if not isinstance(res, list):
            return []
        ret = []
        for index in range(len(res)):
            if len(path) == 1:
                ret = ret + [(res[index].get(path[0]))]
            elif len(path) > 1:
                ret = ret + self.find_field(res[index].get(path[0]), path[1:])
        return ret

    def values_from_path(self, path):
        res = self.res

        if not isinstance(path, list):
            raise TypeError('path should be list type, check type!!')

        if not isinstance(res, dict) and not isinstance(res, list):
            raise TypeError('response should be list or dict type, check type!!')

        values = self.find_field(res, path)

        return values

    def value_from_path(self, path):
        #log.logger.info('getting value from response body, path: {}'.format(path))
        res = self.res

        if not isinstance(path, list):
            raise TypeError('path should be list type, check type!!')

        if not isinstance(res, dict) and not isinstance(res, list):
            raise TypeError('response should be list or dict type, check type!!')

        for val in path:
            if val == 'root':
                return res
            else:
                # print('current val: {}, current res: {}'.format(val, res))
                if isinstance(res, dict):
                    res = res.get(val)
                    continue
                elif isinstance(res, list):
                    res = res[0].get(val)
                    continue
        return res

    def status_code_ok(self,status_code):
        return status_code in [200, 201]

    def auth_error(self,status_code):
        return status_code in [400, 401]

    def rec_count_greater_0(self, path):
        value_from_path = self.value_from_path(path)
        #print('data_from_res type: {}'.format(value_from_path))
        if isinstance(value_from_path, list):
            return len(value_from_path) > 0
        elif isinstance(value_from_path, dict):
            return len(value_from_path) > 0
        else:
            return int(value_from_path) > 0


class ExtendAssertion(BaseAssertion):
    def __init__(self, res):
        super(ExtendAssertion, self).__init__(res)

    def keys_equal(self, path, expect):
        log.logger.info('getting value from body, path: {}'.format(path))
        value_from_path = self.value_from_path(path)
        if isinstance(value_from_path, list):
            actual = set(value_from_path[0].keys())
        else:
            actual = set(value_from_path.keys())
        log.logger.info('asserting keys equal,  actual: {}, expect: {}, result: {}'.format(actual, set(expect), actual == set(expect)))
        return actual == set(expect)

    def keys_partial(self, path, expect):
        log.logger.info('getting value from body, path: {}'.format(path))
        value_from_path = self.value_from_path(path)
        if isinstance(value_from_path, list):
            actual = set(value_from_path[0].keys())
        else:
            actual = set(value_from_path.keys())
        if len(actual) >= len(expect):
            log.logger.info('asserting actual is superSet of expect,  actual: {}, expect: {}, result: {}'.format(actual, set(expect), actual.issuperset(set(expect))))
            return actual.issuperset(set(expect))
        else:
            log.logger.info('asserting expect is superSet of actual,  actual: {}, expect: {}, result: {}'.format(actual, set(expect), set(expect).issuperset(actual)))
            return set(expect).issuperset(actual)

    def path_values_partial(self, path, expect):
        log.logger.info('getting values from body, path: {}'.format(path))
        values_from_path = self.values_from_path(path)
        actual = set(values_from_path)
        log.logger.info('asserting expect is superSet of actual,  actual: {}, expect: {}, result: {}'.format(actual, set(expect), set(expect).issuperset(actual)))
        return set(expect).issuperset(actual)

    def path_values_equal(self, path, expect):
        log.logger.info('getting values from body, path: {}'.format(path))
        values_from_path = self.values_from_path(path)
        log.logger.info('asserting equal, actual: {}, expect: {}, result: {}'.format(values_from_path, expect, values_from_path == expect))
        return expect == values_from_path

    def path_value_equal(self, path, expect):
        log.logger.info('getting value from body, path: {}'.format(path))
        value_from_path = self.value_from_path(path)
        if not isinstance(value_from_path, list):
            expect = expect[0]
        log.logger.info('asserting equal,  actual: {}, expect: {}, result: {}'.format(value_from_path, expect, value_from_path == expect))
        return value_from_path == expect

    def list_path_value_equal(self, patha, pathb, expect):
        log.logger.info('getting value from body, path: {}'.format(patha))
        value_from_path = self.value_from_path(patha)

        print('value_from_path: {}'.format(value_from_path))

        actual = set()
        if isinstance(value_from_path,list):
            for e in value_from_path:
                for key in pathb:
                    e = e[key]
                actual.add(e)
        else:
            raise TypeError
        log.logger.info('asserting equal,  actual: {}, expect: {}, result: {}'.format(actual, expect, actual == set(expect)))
        return actual == set(expect)

    def path_value_greater(self, path, expect):
        log.logger.info('getting value from body, path: {}'.format(path))
        value_from_path = self.value_from_path(path)
        print('type: {}, value: {}'.format(type(value_from_path), value_from_path))
        expect = expect[0]
        if isinstance(value_from_path, list):
            actual = len(value_from_path)
        elif isinstance(value_from_path, str):
            actual = int(value_from_path)
        else:
            actual = value_from_path
        log.logger.info('asserting greater,  actual: {}, expect: {}, result: {}'.format(actual, expect, actual > expect))
        return actual > expect

    def path_value_less(self, path, expect):
        log.logger.info('getting value from body, path: {}'.format(path))
        value_from_path = self.value_from_path(path)
        print('type: {}, value: {}'.format(type(value_from_path), value_from_path))
        expect = expect[0]
        if isinstance(value_from_path, list):
            actual = len(value_from_path)
        elif isinstance(value_from_path, str):
            actual = int(value_from_path)
        else:
            actual = value_from_path
        log.logger.info('asserting less,  actual: {}, expect: {}, result: {}'.format(actual, expect, actual < expect))
        return actual < expect

    def path_value_between(self, path, expect):
        log.logger.info('getting values from body, path: {}'.format(path))
        values_from_path = self.values_from_path(path)
        # print('type: {}, value: {}'.format(type(values_from_path), values_from_path))
        min_actual = min(values_from_path)
        max_actual = max(values_from_path)
        expect.sort()
        min_expect = expect[0]
        max_expect = expect[1]

        if min_expect > max_expect:
            min_expect, max_expect = max_expect, min_expect

        log.logger.info('asserting value between,  min_actual: {}, max_actual: {}, min_expect: {}, max_expect: {}, result: {}'.format(min_actual, max_actual, min_expect, max_expect, min_actual >= min_expect and max_actual <= max_expect))
        return min_actual >= min_expect and max_actual <= max_expect

    def path_match_schema(self, path, schema):
        log.logger.info('getting value from body, path: {}'.format(path))
        value_from_path = self.value_from_path(path)
        print('type: {}, value: {}'.format(type(value_from_path), value_from_path))
        try:
            validate(value_from_path, schema)
        except ValidationError as e:
            message = str(e)#.split('\n')[0]
            raise e("schema not match!!", message)
        else:
            return True

    def path_value_match_reg(self, path, pattern):
        log.logger.info('getting value from body, path: {}'.format(path))
        value_from_path = self.value_from_path(path)
        log.logger.info('testing pattern: {}'.format(pattern))

        try:
            value_from_path+' '
        except TypeError:
            print('value_from_path: {} not a str object'.format(value_from_path))

        reg = re.match(pattern,value_from_path)
        log.logger.info(
            'asserting value: {} should match regex: {}, result:{}'.format(value_from_path, pattern, True if reg else False))
        return True if reg else False

    def res_list_match_reg(self, key, pattern):
        res = self.res
        if isinstance(res, list):
            for e in res:
                data = str(e[key])
                #print('data: {}, pattern: {}'.format(data, pattern))
                reg = re.match(pattern, data)

                if not reg:
                    log.logger.info(
                        'asserting value: {} should match regex: {}, result:false'.format(data, pattern))
                    return False
            log.logger.info(
                'asserting list key: {} , match regex: {}, result: true'.format(key, pattern))
            return True
        else:
            raise TypeError('res should be a list!!')


if __name__ == '__main__':
    pass


