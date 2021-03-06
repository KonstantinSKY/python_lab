import functools
import json


def to_json(func):            # Decorator to json
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return json.dumps(func(*args, **kwargs))

    return inner

  