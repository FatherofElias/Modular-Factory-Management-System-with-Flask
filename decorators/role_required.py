from functools import wraps
from flask import jsonify, current_app
from flask_jwt_extended import get_jwt

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            current_app.logger.debug(f"JWT Claims: {claims}")
            if "role" not in claims:
                current_app.logger.error("Role claim is missing in the JWT")
                return jsonify({"message": "Access denied: Role claim is missing"}), 403
            if claims["role"] != role:
                current_app.logger.error(f"User role {claims['role']} does not match required role {role}")
                return jsonify({"message": "Access denied: Insufficient role"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
