import functools
from flask import request


USERS = {
    'namex-ixpqos-ro': 'RO',
    'namex-ixpqos-rw': 'RW',
}

def api_auth_read(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if request.headers.get("X-API-Key"):
            api_key = request.headers.get("X-API-Key")
        else:
            return {"error": "Please provide an API key"}, 400
        # Check if API key is correct and valid
        if api_key in USERS.keys():
            return func(*args, **kwargs)
        else:
            return {"error": "The provided API key is not valid"}, 403
    return decorator

def api_auth_write(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if request.headers.get("X-API-Key"):
            api_key = request.headers.get("X-API-Key")
        else:
            return {"error": "Please provide an API key"}, 400
        # Check if API key is correct and valid
        if api_key in USERS.keys() and USERS[api_key] == 'RW':
            return func(*args, **kwargs)
        else:
            return {"error": "The provided API key has no write privileges"}, 403
    return decorator