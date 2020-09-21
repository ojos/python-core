from typing import Any, List

from .decorator import logging


@logging
def lazy_loader(name: str) -> Any:
    mod: Any
    try:
        mod = __import__(name)
    except ModuleNotFoundError:
        mod_list: List[str] = name.split(".")
        mod = __import__(".".join(mod_list[:-1]))

    components: List[str] = name.split(".")
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod
