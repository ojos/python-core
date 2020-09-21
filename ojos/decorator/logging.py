import functools
from logging import Logger, getLogger
from typing import Any, Callable


def logging(func: Callable = None, method: str = "DEBUG"):
    if func is None:
        return functools.partial(logging, method=method)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger: Logger = getLogger("{}.{}".format(func.__module__, func.__name__))
        logging: Callable = getattr(logger, str.lower(method))

        logging("START")
        logging("INPUT <args:{}, kwargs:{}>".format(args, kwargs))
        res: Any = func(*args, **kwargs)
        logging("RETURN: <{}>".format(res))
        logging("END")
        return res

    return wrapper
