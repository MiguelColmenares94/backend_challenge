from flask import Flask, jsonify
from flask_cors import CORS
from flask_smorest import Api
from dotenv import load_dotenv
import os

from .shared.db import db
from .shared.exceptions import AppError


def create_app(test_config=None):
    load_dotenv()

    app = Flask(__name__)

    app.config["DATABASE_URL"] = os.getenv("DATABASE_URL", "sqlite:///sqlite.db")
    app.config["ENV"] = os.getenv("FLASK_ENV", "development")
    app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "0") == "1"

    if test_config:
        app.config.update(test_config)

    CORS(
        app,
        resources={
            r"/*": {
                "origins": "*",
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            }
        },
    )

    app.url_map.strict_slashes = False

    app.config["API_TITLE"] = "Contacts API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )

    db.init_app(app.config["DATABASE_URL"])

    api = Api(app)

    from app.modules.user import user_bp
    from app.modules.health import health_bp

    api.register_blueprint(user_bp)
    api.register_blueprint(health_bp)

    @app.errorhandler(AppError)
    def handle_app_error(error):
        response = {"error": error.message}
        return jsonify(response), error.status_code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app
