from flask import Blueprint


bp = Blueprint("chat", __name__)

from app.chat import views