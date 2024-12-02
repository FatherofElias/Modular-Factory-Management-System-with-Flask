from flask import Blueprint, request, jsonify
from controllers.order_controller import OrderController
from models.schemas.order_schema import OrderSchema
from __init__ import limiter
from decorators.role_required import role_required
from flask_jwt_extended import jwt_required


bp = Blueprint('orders', __name__, url_prefix='/orders')

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

@bp.route('/', methods=['GET'])
@limiter.limit("5 per minute")
def get_orders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    orders = OrderController.get_paginated_orders(page, per_page)
    if orders.items:
        return orders_schema.jsonify(orders.items)
    else:
        return jsonify([])

@bp.route('/<int:order_id>', methods=['GET'])
@limiter.limit("5 per minute")
def get_order(order_id):
    order = OrderController.get_order_by_id(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404
    return order_schema.jsonify(order)

@bp.route('/', methods=['POST'])
@limiter.limit("2 per minute")
def add_order():
    data = request.json
    new_order = OrderController.add_order(data)
    return order_schema.jsonify(new_order), 201

@bp.route('/<int:order_id>', methods=['PUT'])
@limiter.limit("2 per minute")
def update_order(order_id):
    data = request.json
    updated_order = OrderController.update_order(order_id, data)
    if not updated_order:
        return jsonify({'message': 'Order not found'}), 404
    return order_schema.jsonify(updated_order)

@bp.route('/<int:order_id>', methods=['DELETE'])
@limiter.limit("2 per minute")
def delete_order(order_id):
    deleted_order = OrderController.delete_order(order_id)
    if not deleted_order:
        return jsonify({'message': 'Order not found'}), 404
    return order_schema.jsonify(deleted_order)



@bp.route('/save', methods=['POST'])
@jwt_required()
@role_required('admin')
def save_order():
    data = request.get_json()
    response = OrderController.save_order(data)
    return jsonify(response), 201
