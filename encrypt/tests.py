from django.test import TestCase
from encrypt.encrypt import encrypt_by_public_key


class EncryptTests(TestCase):
    def test_encrypt_by_public_key(self):
        print(encrypt_by_public_key("12313", b"abc"))
