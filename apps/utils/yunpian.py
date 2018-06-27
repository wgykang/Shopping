# -*- coding: utf-8 -*-
__author__ = 'yank'
__date__ = '2018/5/28/20:40'

import requests
import json


class YunPian:

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        parmas = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': '【小牛电商】尊敬的用户，您的验证码是{}，非本人操作，请忽略'.format(code)
        }
        response = requests.post(self.single_send_url, data=parmas)
        re_dict = json.loads(response.text)
        return re_dict


# if __name__ == '__main__':
#     yun_pian = YunPian('ca31d1414fab8f9a5351e62a0e87e721')
#     yun_pian.send_sms('2222', '13971039366')
