from flask import Blueprint, request, jsonify
from controllers.production_controller import ProductionController
from models.schemas.production_schema import ProductionSchema
from __init__ import limiter

bp = Blueprint('productions', __name__, url_prefix='/productions')

production_schema = ProductionSchema()
productions_schema = ProductionSchema(many=True)

@bp.route('/', methods=['GET'])
@limiter.limit("5 per minute")
def get_productions():
    productions = ProductionController.get_all_productions()
    return productions_schema.jsonify(productions)

@bp.route('/<int:production_id>', methods=['GET'])
@limiter.limit("5 per minute")
def get_production(production_id):
    production = ProductionController.get_production_by_id(production_id)
    if not production:
        return jsonify({'message': 'Production not found'}), 404
    return production_schema.jsonify(production)

@bp.route('/', methods=['POST'])
@limiter.limit("2 per minute")
def add_production():
    data = request.json
    new_production = ProductionController.add_production(data)
    return production_schema.jsonify(new_production), 201

@bp.route('/<int:production_id>', methods=['PUT'])
@limiter.limit("2 per minute")
def update_production(production_id):
    data = request.json
    updated_production = ProductionController.update_production(production_id, data)
    if not updated_production:
        return jsonify({'message': 'Production not found'}), 404
    return production_schema.jsonify(updated_production)

@bp.route('/<int:production_id>', methods=['DELETE'])
@limiter.limit("2 per minute")
def delete_production(production_id):
    deleted_production = ProductionController.delete_production(production_id)
    if not deleted_production:
        return jsonify({'message': 'Production not found'}), 404
    return production_schema.jsonify(deleted_production)
