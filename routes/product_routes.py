from flask import Blueprint, request, jsonify
from controllers.product_controller import ProductController
from models.schemas.product_schema import ProductSchema
from flask_jwt_extended import jwt_required
from decorators.role_required import role_required
from __init__ import limiter


bp = Blueprint('products', __name__, url_prefix='/products')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@bp.route('/', methods=['GET'])
@limiter.limit("5 per minute")
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    products = ProductController.get_paginated_products(page, per_page)
    if products.items:
        return products_schema.jsonify(products.items)
    else:
        return jsonify([])

@bp.route('/<int:product_id>', methods=['GET'])
@limiter.limit("5 per minute")
def get_product(product_id):
    product = ProductController.get_product_by_id(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    return product_schema.jsonify(product)

@bp.route('/', methods=['POST'])
@limiter.limit("2 per minute")
def add_product():
    data = request.json
    new_product = ProductController.add_product(data)
    return product_schema.jsonify(new_product), 201

@bp.route('/<int:product_id>', methods=['PUT'])
@limiter.limit("2 per minute")
def update_product(product_id):
    data = request.json
    updated_product = ProductController.update_product(product_id, data)
    if not updated_product:
        return jsonify({'message': 'Product not found'}), 404
    return product_schema.jsonify(updated_product)

@bp.route('/<int:product_id>', methods=['DELETE'])
@limiter.limit("2 per minute")
def delete_product(product_id):
    deleted_product = ProductController.delete_product(product_id)
    if not deleted_product:
        return jsonify({'message': 'Product not found'}), 404
    return product_schema.jsonify(deleted_product)



@bp.route('/top-selling', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_top_selling_products():
    top_selling_products = ProductController.identify_top_selling_products()
    return jsonify(top_selling_products)

@bp.route('/save', methods=['POST'])
@jwt_required()
@role_required('admin')
def save_product():
    data = request.get_json()
    response = ProductController.save_product(data)
    return jsonify(response), 201
