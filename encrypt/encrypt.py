import base64
# pip install cryptography==41.0.3
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


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
