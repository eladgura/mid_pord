from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims, verify_jwt_refresh_token_in_request
from jwt import DecodeError

def jwt_needed(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except (ValueError, DecodeError, TypeError):
            return {'error': 'access token error'}, 401

        return func(*args, **kwargs)
    return decorator

def jwt_refresh_token_needed(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            verify_jwt_refresh_token_in_request()
        except (ValueError, DecodeError, TypeError):
            return {'error': 'refresh token error'}, 401

        return func(*args, **kwargs)
    return decorator

def admin_needed(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except (ValueError, DecodeError, TypeError):
            return {'error': 'access token error'}, 401

        claims = get_jwt_claims()
        if claims.get('is_admin'):
            return func(*args, **kwargs)
        else:
            return {'error': 'admin required'}, 403

    return decorator
