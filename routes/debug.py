from flask import Blueprint, request, jsonify
from flask_jwt_extended import decode_token

bp = Blueprint('debug', __name__, url_prefix='/debug')

@bp.route('/decode-token', methods=['POST'])
def decode():
    token = request.json.get('token')
    decoded = decode_token(token)
    return jsonify(decoded), 200
