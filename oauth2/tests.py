from django.test import TestCase
from oauth2.encrypt import sign, timestamp, random_str


class EncryptTests(TestCase):

    def test_sign(self):
        t = timestamp()  # 精确到毫秒
        print("sign:", sign(t, random_str(4), "abc",""))
