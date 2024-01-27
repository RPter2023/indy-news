from cachetools import TTLCache
from cachetools.keys import hashkey

from lib.parameterized_lock import parameterized_lock


def async_threadsafe_ttl_cache(func=None, ttl=60):
    cache = TTLCache(maxsize=100, ttl=ttl)

    def decorator(decorated_func):
        async def wrapper(*args, **kwargs):
            # Does not use 'session' in the key
            kwargs_for_key = {i: kwargs[i] for i in kwargs if i != "session"}
            key = hashkey(*args, **kwargs_for_key)
            if key in cache:
                return cache[key]
            with parameterized_lock(key):
                if key in cache:
                    return cache[key]
                cache[key] = await decorated_func(*args, **kwargs)
                return cache[key]

        return wrapper

    # Allows to call the decorator with or without parenthesis
    return decorator(func) if callable(func) else decorator


def sync_threadsafe_ttl_cache(func=None, ttl=60):
    cache = TTLCache(maxsize=100, ttl=ttl)

    def decorator(decorated_func):
        def wrapper(*args, **kwargs):
            # Does not use 'session' in the key
            kwargs_for_key = {i: kwargs[i] for i in kwargs if i != "session"}
            key = hashkey(*args, **kwargs_for_key)
            if key in cache:
                return cache[key]
            with parameterized_lock(key):
                if key in cache:
                    return cache[key]
                cache[key] = decorated_func(*args, **kwargs)
                return cache[key]

        return wrapper

    # Allows to call the decorator with or without parenthesis
    return decorator(func) if callable(func) else decorator
