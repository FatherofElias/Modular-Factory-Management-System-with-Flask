from models.order import Order
from database import db

class OrderController:
    @staticmethod
    def get_all_orders():
        return Order.query.all()

    @staticmethod
    def get_order_by_id(order_id):
        return Order.query.get(order_id)

    @staticmethod
    def add_order(data):
        new_order = Order(customer_id=data['customer_id'], product_id=data['product_id'], quantity=data['quantity'], total_price=data['total_price'])
        db.session.add(new_order)
        db.session.commit()
        return new_order

    @staticmethod
    def update_order(order_id, data):
        order = Order.query.get(order_id)
        if order:
            order.customer_id = data['customer_id']
            order.product_id = data['product_id']
            order.quantity = data['quantity']
            order.total_price = data['total_price']
            db.session.commit()
        return order

    @staticmethod
    def delete_order(order_id):
        order = Order.query.get(order_id)
        if order:
            db.session.delete(order)
            db.session.commit()
        return order
