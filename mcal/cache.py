import os

_FOLDER_NAME = '_CACHE'


def init_cache():
    os.makedirs(_FOLDER_NAME, exist_ok=True)


def set_value(key, value):
    file_path = os.path.join(_FOLDER_NAME, f'{key}.txt')
    with open(file_path, 'w') as f:
        f.write(str(value))


def get_value(key, fallback=None, return_type=str):
    file_path = os.path.join(_FOLDER_NAME, f'{key}.txt')

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return return_type(f.read())
    else:
        return fallback


def get_report() -> dict:
    keys = os.listdir(_FOLDER_NAME)
    keys = [x.split('.')[0] for x in keys]

    values = [get_value(k) for k in keys]

    cache_dict = dict(zip(keys, values))
    return cache_dict
