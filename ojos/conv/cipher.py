import base64
from typing import Union

import pyaes

from ..decorator import logging


@logging
def encrypt(key: Union[str, bytes], raw: bytes) -> bytes:
    if isinstance(key, str):
        key = key.encode("utf-8")
    cipher: pyaes.AESModeOfOperationCTR = pyaes.AESModeOfOperationCTR(key)
    return base64.urlsafe_b64encode(cipher.encrypt(raw))


@logging
def decrypt(key: Union[str, bytes], enc: bytes) -> bytes:
    if isinstance(key, str):
        key = key.encode("utf-8")
    cipher: pyaes.AESModeOfOperationCTR = pyaes.AESModeOfOperationCTR(key)
    return cipher.decrypt(base64.urlsafe_b64decode(enc))
