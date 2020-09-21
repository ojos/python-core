import time as _time
from datetime import date, datetime, time
from typing import Optional, Union

import pytz
from tzlocal import get_localzone

from ..decorator import logging

LOCAL_ZONE = get_localzone().zone
ISO_FORMAT_PATTERN = r"^\d{4}-\d{2}-\d{2}(( |T)\d{2}:\d{2}:\d{2}(([.,])\d{1,6})?Z?([+-]\d{2}(:)?\d{2})?)?$"


@logging
def as_tz(dt: datetime, zone: str = LOCAL_ZONE) -> datetime:
    if dt.tzinfo is None:
        dt = get_localzone().localize(dt)
    dt = dt.astimezone(pytz.timezone(zone))
    return dt


@logging
def dt_to_int(dt: Union[datetime, date], microsecond: bool = False) -> int:
    if not isinstance(dt, datetime):
        dt = datetime.combine(dt, time())
    i: int = int(_time.mktime(dt.timetuple()))
    if microsecond:
        i = i * 1000 + int(dt.microsecond / 1000)
    return i


@logging
def int_to_dt(
    i: int, microsecond: int = False, zone: Optional[str] = LOCAL_ZONE
) -> datetime:
    dt = as_tz(datetime.fromtimestamp(i / 1000 if microsecond else i), zone)
    return dt


@logging
def now(zone: Optional[str] = LOCAL_ZONE) -> datetime:
    return as_tz(datetime.now(), zone)


@logging
def now_int(microsecond=False, zone: Optional[str] = LOCAL_ZONE) -> int:
    return dt_to_int(now(zone), microsecond)
