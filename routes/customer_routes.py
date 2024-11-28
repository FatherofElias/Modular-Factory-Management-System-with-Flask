from flask import Blueprint, request, jsonify
from controllers.customer_controller import CustomerController
from models.schemas.customer_schema import CustomerSchema
from __init__ import limiter

bp = Blueprint('customers', __name__, url_prefix='/customers')

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

@bp.route('/', methods=['GET'])
@limiter.limit("5 per minute")
def get_customers():
    customers = CustomerController.get_all_customers()
    return customers_schema.jsonify(customers)

@bp.route('/<int:customer_id>', methods=['GET'])
@limiter.limit("5 per minute")
def get_customer(customer_id):
    customer = CustomerController.get_customer_by_id(customer_id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404
    return customer_schema.jsonify(customer)

@bp.route('/', methods=['POST'])
@limiter.limit("2 per minute")
def add_customer():
    data = request.json
    new_customer = CustomerController.add_customer(data)
    return customer_schema.jsonify(new_customer), 201

@bp.route('/<int:customer_id>', methods=['PUT'])
@limiter.limit("2 per minute")
def update_customer(customer_id):
    data = request.json
    updated_customer = CustomerController.update_customer(customer_id, data)
    if not updated_customer:
        return jsonify({'message': 'Customer not found'}), 404
    return customer_schema.jsonify(updated_customer)

@bp.route('/<int:customer_id>', methods=['DELETE'])
@limiter.limit("2 per minute")
def delete_customer(customer_id):
    deleted_customer = CustomerController.delete_customer(customer_id)
    if not deleted_customer:
        return jsonify({'message': 'Customer not found'}), 404
    return customer_schema.jsonify(deleted_customer)



@bp.route('/lifetime-value', methods=['GET'])
@limiter.limit("5 per minute")
def get_customer_lifetime_value():
    threshold = request.args.get('threshold', 500, type=float)  
    lifetime_value_data = CustomerController.determine_customer_lifetime_value(threshold)
    return jsonify(lifetime_value_data)
