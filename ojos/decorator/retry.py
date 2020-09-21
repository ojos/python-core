import functools
import time
from logging import getLogger
from typing import Any, Callable, Tuple

logger = getLogger(__name__)


def retry_handler(exception: Exception, remaining: int, delay: int) -> None:
    logger.warning(
        'Caught "{}", {} tries remaining, sleeping for {} seconds'.format(
            exception, remaining, delay
        )
    )


def retry(
    func: Callable = None,
    max: int = 3,
    delay: int = 1,
    backoff: int = 2,
    exceptions: Tuple = (Exception,),
    hook: Callable = retry_handler,
) -> Any:
    if func is None:
        return functools.partial(
            retry,
            max=max,
            delay=delay,
            backoff=backoff,
            exceptions=exceptions,
            hook=hook,
        )

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        _delay: int = delay
        tries: list = list(range(max))
        tries.reverse()
        for remaining in tries:
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                if remaining > 0:
                    if hook is not None:
                        hook(e, remaining, _delay)
                    time.sleep(_delay)
                    _delay = _delay * backoff
                else:
                    raise

    return wrapper
