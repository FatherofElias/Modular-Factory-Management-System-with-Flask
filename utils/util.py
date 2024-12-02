import jwt
import datetime
from flask import current_app

def encode_token(user_id):
    try:
        payload = {
            'exp': datetime.datetime.now() + datetime.timedelta(days=1), 
            'iat': datetime.datetime.now(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode_token(token):
    try:
        payload = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Token has expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'
