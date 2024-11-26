from flask import Flask
from database import db
from schema import ma

from models.customer import Customer
from models.employee import Employee
from models.order import Order
from models.product import Product
from models.production import Production

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(f'config.{config_name}')
    db.init_app(app)
    ma.init_app(app)

    return app

if __name__ == '__main__':
    app =  create_app('DevelopmentConfig')

    with app.app_context():
        db.drop_all()
        db.create_all()

    app.run(debug=True)