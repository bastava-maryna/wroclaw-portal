"""Class to build api swagger documentation"""
from flask import current_app
from flask_restful import Resource, fields
from main import Api
from config import Config
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    current_app.config["SWAGGER_URL"],
    current_app.config["API_URL"],
    config={"app_name": "WROCLAW PORTAL"},
)
