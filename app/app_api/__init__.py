from flask import Blueprint

api = Blueprint("app_api", __name__)

from app.app_api import auth, enterprise, department
