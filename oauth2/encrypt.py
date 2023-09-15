import base64
# pip install cryptography==41.0.3
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

import logging

import requests
import random
import string
import datetime

import time
import json

from apscheduler.schedulers.background import BackgroundScheduler
from gmssl import sm4, sm3

import sys

sys.path.append("..")
from zhdn import schemas
from apscheduler.schedulers.blocking import BlockingScheduler

from AuthorizationProvider import encrypt_by_public_key

from requests import request

'''
gmssl==3.2.2  
pycryptodomex==3.18.0 
requests
pip3 install apscheduler
'''
# =========== 日志 ==========
# logging.basicConfig(level=logging.DEBUG,filename='log.log', format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')

# =========== 零代码平台配置 ==========
_APP_ID = "631aac0ae4b0533b2211f998"
_AUTH = "xnX6BLGyaw8LquV1ddaxPflIya4968sG"
_EXCLUDE_FIELDS = ("recordId", "userId", "appId",
                   "formId", "updateTime", "applyTime",
                   "ipAddr", "openId",
                   "ipRelationAddress", "systemType", "deviceType",
                   "browserType", "browserVersion", "isMobile", "engineType",
                   "engineVersion", "openId", "title",
                   "archiveStatus", "formRunStatus")

_QUERY_DATA_URL = "http://szxms.biem.edu.cn/openapi/v2/app/form/advance/data_filter"

# ===========  智慧大脑配置  ===========
_ACCESS_TOKEN = ''
_REFRESH_TOKEN = ''
_CHECK_INTERVAL = 30  # 检查登录周期 秒
_APP_KEY = "2bMp2LBC"
_APP_SEC = "********"
_SVR_BASE_URL = "http://202.205.188.198:9000"
_SVR_REFRESH = {"path": "/prod-api4/api/web/auth/login/interface/refresh", "method": "post"}
_SVR_LOGIN = {"path": "/prod-api4/api/web/auth/login/interface/oauth", "method": "post"}
_SVR_GET_REST = {"path": "/prod-api4/api/web/convergence/collect/interface/getResultsByTime", "method": "post"}
_SVR_SAVE_DATA = {"path": "/prod-api4/api/web/convergence/collect/interface/saveInterfaceData", "method": "post"}
# 用户信息
_SVR_USER = {
    "grant_type": "password",
    "client_id": "1",
    "username": "bjjjglzyxy",
    "password": "tKQYxmWOMMewxO9v"
}
_SVR_LOGIN_INFO = {
    "access_token": "",
    "refresh_token": "",
    "expires_time": 0,
    "expires_in": 299,
    "refresh_expires_in": 2592000,
    "client_id": "1",
    "username": "bjjjglzyxy",
    "scope": "",
    "openid": "",
    "app_secret": "",
    "client_secret": "dataCenterInterface@2021"
}

GET_RSA = {
    "path": "/prod-api4/api/web/auth/login/getRSA",
    "method": "get"
}
public_key = request(GET_RSA['method'], url=_SVR_BASE_URL + GET_RSA['path']).json()['returnData']


# =========== 加密/签名相关 ===========
def sm3_hash(message):
    return sm3.sm3_hash([i for i in message.encode(encoding="utf-8")])


def sm4_hash(key: str, data: str):
    sm4Alg = sm4.CryptSM4()
    sm4Alg.set_key(key.encode(encoding="utf-8"), sm4.SM4_ENCRYPT)
    enRes = sm4Alg.crypt_ecb(data.encode())
    return enRes.hex()


# 获取sign
def sign(timestamps: str, r_str: str, data: str):
    return sm3_hash(data + timestamps + r_str)


# 加密数据
def extracted(app_secret: str, data: str):
    return sm4_hash(app_secret[4:20], data)


def random_str(len: int):
    return ''.join(random.choices(string.ascii_uppercase
                                  + string.ascii_lowercase + string.digits, k=len))


# 上报数据接口
def put_data(data: str, header):
    return requests.request(_SVR_SAVE_DATA['method'], url=_SVR_BASE_URL + _SVR_SAVE_DATA['path']
                            , json={"cipherText": data}, headers=header).json()


# 查询数据接口
def get_data(data: str, header):
    return requests.request(_SVR_SAVE_DATA['method'], url=_SVR_BASE_URL + _SVR_GET_REST['path']
                            , json={"cipherText": data}, headers=header).json()


def timestamp():
    return str(int(time.time() * 1000))


def encrypt_by_public_key(data: str, public_key_str):
    print(data, public_key_str)
    public_key_bytes = base64.b64decode(public_key_str)
    key = serialization.load_der_public_key(public_key_bytes,
                                            backend=default_backend())
    cipher = key.encrypt(
        data.encode(encoding="utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ))
    return base64.b64encode(cipher).decode(encoding="utf-8")
