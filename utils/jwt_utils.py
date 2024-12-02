from flask_jwt_extended import create_access_token, get_jwt_identity


def generate_token(user):
    payload = {
        "id": user.id,
        "username": user.username,
        "role": user.role  
    }
    return create_access_token(identity=payload)

def get_current_user():
    return get_jwt_identity()
