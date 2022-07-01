from flask import Flask

def create_app(config_name):
    from .api import api as api_blueprint
    app = Flask(__name__)
    app.register_blueprint(api_blueprint, url_prefix='/api/v1/')
    return app