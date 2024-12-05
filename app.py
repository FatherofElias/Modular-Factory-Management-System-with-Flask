from __init__ import create_app, db
from flask_swagger_ui import get_swaggerui_blueprint
import os



def run():
    app = create_app('DevelopmentConfig')

    with app.app_context():
        db.create_all()


    SWAGGER_URL = '/api/docs' 
    API_URL = '/static/swagger.yaml' 

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={ 
            'app_name': "Factory Management System API"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route('/static/swagger.yaml')
    def swagger_yaml():
        yaml_path = os.path.join(os.path.dirname(__file__), 'static/swagger.yaml')
        with open(yaml_path, 'r') as file:
            return file.read(), 200, {'Content-Type': 'application/x-yaml'}


    return app

if __name__ == '__main__':
    app = run()
    app.run(debug=True)

