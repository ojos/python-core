import json
from logging import INFO, Logger, getLogger
from typing import Any

from ojos.misc import now

logger: Logger = getLogger()
logger.setLevel(INFO)


def json_response(
    status_code: int = 200,
    message: str = "OK",
    content: Any = None,
    headers: dict = {"Content-Type": "application/json; charset=utf-8"},
) -> dict:
    context = {"message": message, "servertime": now().isoformat()}
    if content is not None:
        context["content"] = content
    return {
        "statusCode": status_code,
        "headers": headers,
        "body": json.dumps(context),
    }
