_runtime_cache = dict()


def set_value(key: str, image):
    _runtime_cache[key] = image


def get_value(key: str):
    return _runtime_cache.get(key, None)


def has_key(key: str) -> bool:
    return key in _runtime_cache