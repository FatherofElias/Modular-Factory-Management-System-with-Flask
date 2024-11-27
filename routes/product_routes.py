from flask import Blueprint, request, jsonify
from controllers.product_controller import ProductController
from models.schemas.product_schema import ProductSchema
from __init__ import limiter

bp = Blueprint('products', __name__, url_prefix='/products')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@bp.route('/', methods=['GET'])
@limiter.limit("5 per minute")
def get_products():
    products = ProductController.get_all_products()
    return products_schema.jsonify(products)

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
