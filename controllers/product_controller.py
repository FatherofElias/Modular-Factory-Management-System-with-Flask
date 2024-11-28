from models.product import Product
from database import db
from sqlalchemy import func
from models.order import Order



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
        pagination = Product.query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination
    

    @staticmethod
    def identify_top_selling_products():
        result = db.session.query(
            Product.name.label('product_name'),
            func.sum(Order.quantity).label('total_quantity_ordered')
        ).join(Order, Product.id == Order.product_id
        ).group_by(Product.name
        ).order_by(func.sum(Order.quantity).desc()).all()
        

        top_selling_products = [
            {"product_name": row.product_name, "total_quantity_ordered": row.total_quantity_ordered}
            for row in result
        ]

        return top_selling_products


