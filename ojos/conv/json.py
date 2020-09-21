import re
from datetime import datetime
from typing import Any

from ..decorator import logging
from .datetime import ISO_FORMAT_PATTERN, as_tz

iso_format = re.compile(ISO_FORMAT_PATTERN)


@logging
def serialize(obj: Any) -> Any:
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Object of type {} is not JSON serializable".format(type(obj)))


@logging
def deserialize(obj: dict) -> dict:
    for (key, val) in obj.items():
        if isinstance(val, str) and iso_format.match(val):
            val = val.replace("Z", "+00:00")
            obj[key] = as_tz(datetime.fromisoformat(val))
    return obj
