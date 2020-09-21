from typing import Optional

from ..decorator import logging

NUMERIC = "".join([chr(i) for i in range(48, 57)])  # 0-9
UPPER = "".join([chr(i) for i in range(65, 91)])  # A-Z
LOWER = "".join([chr(i) for i in range(97, 123)])  # a-z


@logging
def encode(n: int, length: int = 10, chars: Optional[str] = None) -> str:
    if chars is None:
        chars = NUMERIC + UPPER + LOWER
    s: str = ""
    while n != 0:
        s = chars[int(n % len(chars))] + s
        n = n - n % len(chars)
        n = int(n / len(chars))
    return (chars[0] * (length - len(s))) + s


@logging
def decode(s: str, chars: Optional[str] = None) -> int:
    if chars is None:
        chars = NUMERIC + UPPER + LOWER
    s = s.lstrip(chars[0])
    n: int = 0
    for c in s:
        n = n * len(chars)
        n = n + chars.index(c)
    return n
