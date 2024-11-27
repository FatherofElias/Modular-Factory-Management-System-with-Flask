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

    from routes.customer_routes import bp as customer_bp
    from routes.employee_routes import bp as employee_bp
    from routes.order_routes import bp as order_bp
    from routes.product_routes import bp as product_bp
    from routes.production_routes import bp as production_bp

    app.register_blueprint(customer_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(production_bp)

    return app

if __name__ == '__main__':
    app = create_app('DevelopmentConfig')

    with app.app_context():
        db.drop_all()
        db.create_all()

    app.run(debug=True)