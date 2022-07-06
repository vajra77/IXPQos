import functools
from flask import request
from ixpqos.app.config import APP_CONFIG


def api_auth(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if request.headers.get("X-API-Key"):
            api_key = request.headers.get("X-API-Key")
        else:
            return {"error": "Please provide an API key"}, 400
        # Check if API key is correct and valid
        if api_key == APP_CONFIG['apikey']:
            return func(*args, **kwargs)
        else:
            return {"error": "The provided API key is not valid"}, 403
    return decorator