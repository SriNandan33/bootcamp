from flask import Blueprint

bp = Blueprint('setup', __name__)

from app.setup import views