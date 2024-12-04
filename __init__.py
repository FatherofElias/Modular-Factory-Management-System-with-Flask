from flask import Flask
from flask_cors import CORS
from database import db
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from controllers.jwt_controller import setup_jwt_routes
from routes.debug import bp as debug_bp
from flask_swagger_ui import get_swaggerui_blueprint


    

limiter = Limiter(key_func=get_remote_address)
ma = Marshmallow()



def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    jwt = JWTManager(app)
    app.config.from_object(f'config.{config_name}')
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'


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
    app.register_blueprint(user_bp)
    app.register_blueprint(debug_bp)  

    
    setup_jwt_routes(app)

    return app

