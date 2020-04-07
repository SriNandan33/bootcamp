from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import Config
from sendgrid import SendGridAPIClient
from app.pusher import Pusher
# extensions
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
moment = Moment()
mail = SendGridAPIClient(Config.SENDGRID_API_KEY)
pusher = Pusher()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail = SendGridAPIClient(Config.SENDGRID_API_KEY)
    moment.init_app(app)
    pusher.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.core import bp as core_bp
    app.register_blueprint(core_bp)

    from app.chat import bp as chat_bp
    app.register_blueprint(chat_bp, url_prefix="/chat")

    return app

from app import models