# -*- coding: utf-8 -*- 
__author__ = 'yank'
__date__ = '2018/6/22/17:28'

from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
from urllib.parse import quote_plus
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
from base64 import decodebytes, encodebytes

import json


class AliPay(object):
    """
    支付宝支付接口
    """

    def __init__(self, appid, app_notify_url, app_private_key_path,
                 alipay_public_key_path, return_url, debug=False):
        # 沙箱环境appid
        self.appid = appid
        # 支付结果异步通知
        self.app_notify_url = app_notify_url
        # 私钥文件路径
        self.app_private_key_path = app_private_key_path
        # 私钥
        self.app_private_key = None
        # 支付页面支付后,进行页面跳转
        self.return_url = return_url
        # 打开私钥文件,然后读取私钥
        with open(self.app_private_key_path) as fp:
            self.app_private_key = RSA.importKey(fp.read())

        # 支付宝公钥
        self.alipay_public_key_path = alipay_public_key_path
        # 打开支付宝公钥文件,读取公钥
        with open(self.alipay_public_key_path) as fp:
            self.alipay_public_key = RSA.import_key(fp.read())

        # 为True是调试环境,选用支付宝沙盒环境
        if debug is True:
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        else:
            self.__gateway = "https://openapi.alipay.com/gateway.do"

    # 请求参数(这是与订单相关的必填4个字段)
    def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):
        biz_content = {
            "subject": subject,
            "out_trade_no": out_trade_no,
            "total_amount": total_amount,
            "product_code": "FAST_INSTANT_TRADE_PAY",
            # "qr_pay_mode":4
        }

        biz_content.update(kwargs)
        # 调用build_body()函数,获取data
        data = self.build_body("alipay.trade.page.pay", biz_content, self.return_url)
        # 对data进行签名
        return self.sign_data(data)

    # 公共请求参数
    def build_body(self, method, biz_content, return_url=None):
        data = {
            "app_id": self.appid,
            "method": method,
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "biz_content": biz_content
        }

        if return_url is not None:
            data["notify_url"] = self.app_notify_url
            data["return_url"] = self.return_url

        return data

    # 签名函数
    def sign_data(self, data):
        # 删除sign
        data.pop("sign", None)
        # 排序后的字符串,调用ordered_data()函数
        unsigned_items = self.ordered_data(data)
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        # 调用sign()函数,进行签名
        sign = self.sign(unsigned_string.encode("utf-8"))
        # ordered_items = self.ordered_data(data)
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in unsigned_items)

        # 获得最终的订单信息字符串
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    # 对参数排序,生产一个tuple
    def ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    # 对跳转的地址进行验证,防止被攻击,验证签名
    def sign(self, unsigned_string):
        # 开始计算签名
        key = self.app_private_key
        # 拿到私钥，然后使用PKCS1_v1_5进行签名,生成签名对象signer
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA256.new(unsigned_string))
        # base64 编码，转换为unicode表示并移除回车
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        return sign

    def _verify(self, raw_content, signature):
        # 开始计算签名
        key = self.alipay_public_key
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(raw_content.encode("utf8"))
        if signer.verify(digest, decodebytes(signature.encode("utf8"))):
            return True
        return False

    def verify(self, data, signature):
        if "sign_type" in data:
            sign_type = data.pop("sign_type")
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
        return self._verify(message, signature)


if __name__ == "__main__":
    return_url = 'http://127.0.0.1:8000/alipay/return/?charset=utf-8&out_trade_no=20170202839&method=alipay.trade.page.pay.return&total_amount=120.00&sign=YSeXjS2HlQWxVLA7yfRSIt9pAgQTw55qPxXq6za%2FAk54yUncGwfrQbgbQR0tg1oE5RFQw5A0YnPt%2FuIcDzk7wGRX8n6%2FDrXe6PpEitHVEVsB9aMcPk8Gmq%2FTwaqjF675WslSxtM4uLau98Fxbr7uLfq2GMvEmCPXe22n5wEpufzGXnnqV7zAy3Yxy3Thl0Yg4NAaVMPL%2FSivmBkVlLjfaZQWCd6IGh8g0V9t5RF6lcU9d%2FWNPN337E7B3i7VsFiajr890aizkqQ%2BqtsTYYG7Evn2Pa3%2FoRRvjEwA029E1wJEK%2FEwvyMk5HfzilrehhBr3GzZt7cdwcrCo7HgQ2Bx6A%3D%3D&trade_no=2018062221001004680200385241&auth_app_id=2016091400506463&version=1.0&app_id=2016091400506463&sign_type=RSA2&seller_id=2088102175537047&timestamp=2018-06-22+19%3A50%3A24'
    o = urlparse(return_url)
    query = parse_qs(o.query)
    processed_query = {}
    ali_sign = query.pop("sign")[0]

    # 测试订单支付
    alipay = AliPay(
        # 支付宝开发平台沙箱环境默认生成
        appid="2016091400506463",
        # vue联调使用
        app_notify_url="http://203.195.162.142:8000/alipay/return/",
        # 私钥
        app_private_key_path="../trade/keys/siyao_2048.txt",
        # 支付宝公钥
        alipay_public_key_path="../trade/keys/alipay_2048.txt",  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        # 为True使用沙箱的url
        debug=True,  # 默认False
        return_url="http://203.195.162.142:8000/alipay/return/"
    )

    for key, value in query.items():
        processed_query[key] = value[0]
    print(alipay.verify(processed_query, ali_sign))

    # 生成请求的字符集
    url = alipay.direct_pay(
        # 订单标题
        subject="测试订单2",
        # 订单号
        out_trade_no="2018181816",
        # 金额
        total_amount=120,
        return_url="http://203.195.162.142:8000/alipay/return/"
    )
    # 拼接URL
    re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

    print(re_url)
