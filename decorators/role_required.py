from functools import wraps
from jwt import verify_jwt_in_request, get_jwt
from flask import jsonify

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] != role:
                return jsonify({"message": "Access denied"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
