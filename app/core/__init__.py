from flask import Blueprint

bp = Blueprint('core', __name__)

from app.core import views