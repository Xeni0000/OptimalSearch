import random

from datetime import datetime, timezone

SIMPLE_TOKEN_CHARS = '123456789ABCDEFGHJKLMNPQRSTUVWXYZ'
KEY_CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'


def random_id(size: int):
    return ''.join(random.choice(SIMPLE_TOKEN_CHARS) for _ in range(size))


def random_key(size: int):
    return ''.join(random.choice(KEY_CHARS) for _ in range(size))


def now_utc():
    return datetime.now(timezone.utc)
