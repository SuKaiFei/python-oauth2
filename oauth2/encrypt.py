import json
import random
import string
import time

# pip install gmssl==3.2.2
from gmssl import sm4, sm3
# pip install requests==2.31.0
from requests import request
from oauth2.AuthorizationProvider import encrypt_by_public_key


def sm3_hash(message):
    return sm3.sm3_hash([i for i in message.encode(encoding="utf-8")])


def timestamp():
    return str(int(time.time() * 1000))


def random_str(random_len: int):
    return ''.join(random.choices(string.ascii_uppercase +
                                  string.ascii_lowercase + string.digits, k=random_len))


def sign(timestamps: str, r_str: str, data: str, secret: str):
    return sm3_hash(secret + data + timestamps + r_str + secret)
