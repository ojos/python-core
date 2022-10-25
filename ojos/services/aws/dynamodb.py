import base64
import pickle
import urllib.parse
from io import BytesIO
from logging import INFO, Logger, getLogger
from typing import TypedDict

logger: Logger = getLogger()
logger.setLevel(INFO)


class StringAttribute(TypedDict):
    S: str


class NumberAttribute(TypedDict):
    N: str


class LastEvaluatedKey(object):
    @staticmethod
    def encode(last_evaluated_key: dict):
        file = BytesIO()
        pickle.dump(last_evaluated_key, file)
        file.seek(0)
        encoded = base64.urlsafe_b64encode(file.read())
        return urllib.parse.quote(encoded.decode())

    @staticmethod
    def decode(hash: str):
        file = BytesIO()
        file.write(base64.b64decode(urllib.parse.unquote(hash)))
        file.seek(0)
        return pickle.load(file)
