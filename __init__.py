from flask import Flask
from database import db
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_marshmallow import Marshmallow
from jwt import JWTManager

limiter = Limiter(key_func=get_remote_address)
ma = Marshmallow()
jwt = JWTManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    db.init_app(app)
    limiter.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    from routes.customer_routes import bp as customer_bp
    from routes.employee_routes import bp as employee_bp
    from routes.order_routes import bp as order_bp
    from routes.product_routes import bp as product_bp
    from routes.production_routes import bp as production_bp
    from routes.user_routes import bp as user_bp  

    app.register_blueprint(customer_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(production_bp)
    app.register_blueprint(user_bp)  # Add this line

    return app
