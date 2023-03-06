from flask import Flask

def create_app():
    app = Flask(__name__)

    from src.views import app_routes

    app.register_blueprint(app_routes, url_prefix="/")

    return app

