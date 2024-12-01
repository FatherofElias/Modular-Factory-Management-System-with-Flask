from flask import Blueprint, request, jsonify
from models.user import User
from __init__ import db
from utils.jwt_utils import generate_token, get_jwt_identity
from jwt import jwt_required

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
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = generate_token(user.id, user.role)
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    current_user = get_jwt_identity()
    return jsonify(current_user), 200
