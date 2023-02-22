#coding:utf-8
from com.config import Config
from com.log import Logger
import logging
import pytest
import os
import sys
import json
from com.my_redis import Redi
from com.parse_csv import  Csvparser
from com.config import Config
from com.mhttp import Request


c = Config()
redi = Redi()
request = Request()
debug = c.get_config('DEFAULT', 'DEBUG')
log = Logger(__name__, CmdLevel=logging.INFO, FileLevel=logging.INFO)

'''
class Run(object):
    def run(self):
        try:
            redi.get(None)
            print('Successfully connected to redis')
        except ConnectionError:
            print('Redis connection error')
            sys.exit()

        os.system(r"cp allure-report/history/* allure-results/history")
        # os.system(r"rm -f allure-results/*")
        os.system(r'find allure-results/ -maxdepth 0 -type f -delete')
        pytest.main(["-v", "-s", 'tc/', "--alluredir", "./allure-results"])
        os.system(r"allure generate --clean allure-results -o allure-report")
 '''
def send_run_result_to_slack():
    csv_file_path_from_config = c.get_config('CSV', 'ALLURE_CSV_PATH')
    csv = Csvparser(csv_file_path_from_config)
    data = csv.rows
    jsonbody = dict()
    jsonbody['message'] = 'Hooray'
    jsonbody['username'] = 'API_AUTOMATION'
    jsonbody['text'] = 'automation test finished \n pass: ' + data[0]['PASSED'] + '\n fail: ' + data[0][
        'FAILED'] + '\n broken: ' + data[0]['BROKEN'] + '\n for more details, please visit: http://123.56.139.xxxx:8080/'
    body = json.dumps(jsonbody)
    # 给slack发通知
    request.post('https://hooks.slack.com/services/xxx/xxx/xxxxx',
                 headers={'Content-Type': 'application/json'},
                 data=body)

    CorpID = 'xxx'
    Secret = 'xxxxxxxxx'
    res = request.get('https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + CorpID + '&corpsecret=' + Secret)

    if res.status_code == 200:
        access_token = res.json().get('access_token')
        log.logger.info('get wecom access_token successfully, token: {}'.format(access_token))
        payload = {'touser': 'xxx', 'agentid' : 1000002, 'msgtype': 'text', 'text' : {'content' : None}}
        payload['text']['content'] = body
        payload = json.dumps(payload)
        log.logger.info('get  payload successfully, payload: {}'.format(payload))
        # 给企业微信发通知
        r= request.post('https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='+access_token,
                     data = payload)
        if r.status_code == 200:
            log.logger.info('send to wecom Leap agentid successfully, detail: {}'.format(r.json()))
        else:
            log.logger.info('there might be some wrong sending message to wecom, detail: {}'.format(r.json()))

if __name__ == "__main__":
    '''
    先判断redis能否正常连接
    删除上次执行结果
    跑测试
    生成结果，发送结果至slack和企业微信
    '''
    try:
        redi.get('apikey')
        print('Successfully connected to redis')
    except ConnectionError as e:
        print('Redis connection error')
        sys.exit()

    os.system(r"cp allure-report/history/* allure-results/history")
    # os.system(r"rm -f allure-results/*")
    os.system(r'find allure-results/ -maxdepth 1 -type f -delete')
    pytest.main(["-v", "-s", 'tc/', "--alluredir", "./allure-results"])
    os.system(r"allure generate --clean allure-results -o allure-report")

    if debug == 'False':
        send_run_result_to_slack()



