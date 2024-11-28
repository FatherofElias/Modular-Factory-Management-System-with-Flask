from models.product import Product
from database import db


class ProductController:
    @staticmethod
    def get_all_products():
        return Product.query.all()

    @staticmethod
    def get_product_by_id(product_id):
        return Product.query.get(product_id)

    @staticmethod
    def add_product(data):
        new_product = Product(**data)
        db.session.add(new_product)
        db.session.commit()
        return new_product

    @staticmethod
    def update_product(product_id, data):
        product = Product.query.get(product_id)
        if not product:
            return None
        for key, value in data.items():
            setattr(product, key, value)
        db.session.commit()
        return product

    @staticmethod
    def delete_product(product_id):
        product = Product.query.get(product_id)
        if not product:
            return None
        db.session.delete(product)
        db.session.commit()
        return product

    @staticmethod
    def get_paginated_products(page, per_page):
        return Product.query.paginate(page=page, per_page=per_page)
