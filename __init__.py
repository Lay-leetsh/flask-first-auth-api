from flask import Flask
from flask_restx import Api

from apis.auth.controller.auth_controller import auth_ns
from apis.core.error_handler import error_handle
from apis.users.controller.user_controller import user_ns
from config import Config
from extensions import db, jwt


def create_app():
    # Create the Flask app and configure it with the app configuration object
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # JWT 인증 설정
    authorizations = {
        'jwt': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
        }
    }

    # Initialize the API with the Flask app and set the version and title
    api = Api(
        app,
        version='0.1',
        title='Lay\'s API',
        description='API for managing Lay records',
        prefix='/api/v1/',
        authorizations=authorizations,
        security='jwt'
    )

    # Initialize error handler
    error_handle(api)

    # Add namespace to the API
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(user_ns, path='/users')

    with app.app_context():
        db.create_all()

    return app
