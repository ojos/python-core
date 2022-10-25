from datetime import datetime
from logging import INFO, Logger, getLogger

from dateutil import tz

logger: Logger = getLogger()
logger.setLevel(INFO)


def now(timezone: str = "UTC") -> datetime:
    now = datetime.utcnow().astimezone(tz.gettz("UTC"))
    if timezone != "UTC":
        now.astimezone(tz.gettz(timezone))
    return now
