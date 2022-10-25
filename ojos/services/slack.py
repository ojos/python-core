import hashlib
import hmac
import json
from datetime import datetime
from enum import Enum

import httpx
from ojos.decorator import logging


class Color(Enum):
    RED: str = "#F00"
    GREEN: str = "#0F0"
    BLUE: str = "#00F"


@logging
def verify(secret: str, request_ts: int, signature: str, body: str) -> bool:
    now_ts: int = int(datetime.now().timestamp())
    if abs(request_ts - now_ts) > (60 * 5):
        return False

    message: str = "v0:{}:{}".format(request_ts, body)
    expected: str = "v0={}".format(
        hmac.new(
            bytes(secret, "UTF-8"), bytes(message, "UTF-8"), hashlib.sha256
        ).hexdigest()
    )
    return hmac.compare_digest(expected, signature)


def response(title: str, text: str, color: str = Color.BLUE.value):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "attachments": [
                    {
                        "title": title,
                        "text": text,
                        "color": color,
                        "mrkdwn": True,
                    }
                ],
            }
        ),
    }


@logging
def notify_executed(slack_webhook_url: str, username: str, command: str, text: str):
    title: str = "Command was executed"
    content: str = "User: *{}*\nInput: *{} {}*".format(username, command, text)
    color: str = Color.BLUE.value

    httpx.post(
        slack_webhook_url,
        data=json.dumps(
            {
                "attachments": [
                    {
                        "title": title,
                        "text": content,
                        "color": color,
                        "mrkdwn": True,
                    }
                ],
            }
        ),
        headers={"Content-Type": "application/json"},
    )
