from jwt import create_access_token, get_jwt_identity

def generate_token(user_id, role):
    return create_access_token(identity={"user_id": user_id, "role": role})

def get_current_user():
    return get_jwt_identity()
