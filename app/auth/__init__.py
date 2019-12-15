from flask import Blueprint

auth_bp = Blueprint('data_bp', __name__)

from . import views
