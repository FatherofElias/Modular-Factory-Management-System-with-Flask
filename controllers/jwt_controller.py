from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

class JWTController:

    @staticmethod
    @jwt_required()
    def protected():
        current_user = get_jwt_identity()
        return jsonify({"message": "Welcome!", "user": current_user}), 200

    @staticmethod
    def validate_token(token):
        
        return True

    @staticmethod
    def get_user_by_token(token):
        user_identity = get_jwt_identity()
        return User.query.filter_by(id=user_identity['user_id']).first()


def setup_jwt_routes(app):
    @app.route('/protected', methods=['GET'])
    @jwt_required()
    def protected_route():
        return JWTController.protected()

    @app.route('/validate-token', methods=['POST'])
    def validate_token_route():
        token = request.json.get('token')
        if JWTController.validate_token(token):
            return jsonify({"message": "Token is valid"}), 200
        else:
            return jsonify({"message": "Token is invalid"}), 400
