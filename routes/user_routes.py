from flask import Blueprint, request, jsonify
from models.user import User
from __init__ import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        role=data['role']
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        user_id = user.id
        user_role = user.role
        additional_claims = {"role": user_role}
        access_token = create_access_token(identity=user_id, additional_claims=additional_claims, expires_delta=timedelta(minutes=60))
        return jsonify(access_token=access_token)
    return jsonify({"message": "Invalid credentials"}), 401


@bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    current_user = get_jwt_identity()
    return jsonify(current_user), 200
