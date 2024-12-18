from models.order import Order
from database import db
from decorators.role_required import role_required



class OrderController:
    @staticmethod
    def get_all_orders():
        return Order.query.all()

    @staticmethod
    def get_order_by_id(order_id):
        return Order.query.get(order_id)

    @staticmethod
    def add_order(data):
        new_order = Order(**data)
        db.session.add(new_order)
        db.session.commit()
        return new_order

    @staticmethod
    def update_order(order_id, data):
        order = Order.query.get(order_id)
        if not order:
            return None
        for key, value in data.items():
            setattr(order, key, value)
        db.session.commit()
        return order

    @staticmethod
    def delete_order(order_id):
        order = Order.query.get(order_id)
        if not order:
            return None
        db.session.delete(order)
        db.session.commit()
        return order

    @staticmethod
    def get_paginated_orders(page, per_page):
        pagination = Order.query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination


    @staticmethod
    @role_required('admin')
    def save_order(data):
        new_order = Order(
            customer_id=data['customer_id'],
            product_id=data['product_id'],
            quantity=data['quantity'],
            total_price=data['total_price']
        )
        db.session.add(new_order)
        db.session.commit()
        return {"message": "Order saved successfully"}

