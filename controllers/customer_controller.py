from models.customer import Customer
from database import db
from sqlalchemy import func
from models.order import Order
from decorators.role_required import role_required


class CustomerController:
    @staticmethod
    def get_all_customers():
        return Customer.query.all()

    @staticmethod
    def get_customer_by_id(customer_id):
        return Customer.query.get(customer_id)

    @staticmethod
    def add_customer(data):
        new_customer = Customer(name=data['name'], email=data['email'], phone=data['phone'])
        db.session.add(new_customer)
        db.session.commit()
        return new_customer

    @staticmethod
    def update_customer(customer_id, data):
        customer = Customer.query.get(customer_id)
        if customer:
            customer.name = data['name']
            customer.email = data['email']
            customer.phone = data['phone']
            db.session.commit()
        return customer

    @staticmethod
    def delete_customer(customer_id):
        customer = Customer.query.get(customer_id)
        if customer:
            db.session.delete(customer)
            db.session.commit()
        return customer
    

    @staticmethod
    @role_required('admin')
    def save_customer(data):
        new_customer = Customer(
            name=data['name'],
            email=data['email'],
            phone=data['phone']
        )
        db.session.add(new_customer)
        db.session.commit()
        return {"message": "Customer saved successfully"}

    @staticmethod
    @role_required('admin')
    def determine_customer_lifetime_value(threshold):
        result = db.session.query(
            Customer.name.label('customer_name'),
            func.sum(Order.total_price).label('total_order_value')
        ).join(Order, Customer.id == Order.customer_id
        ).group_by(Customer.name
        ).having(func.sum(Order.total_price) >= threshold).all()
        
    
        lifetime_value_data = [
            {"customer_name": row.customer_name, "total_order_value": row.total_order_value}
            for row in result
        ]

        return lifetime_value_data

