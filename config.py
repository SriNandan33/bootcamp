import os

BASE_DIR = os.path.abspath(os.path.dirname(__name__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is-less-secure'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 25
    # mail config
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')

    # pusher config
    PUSHER_APP_ID = os.environ.get('PUSHER_APP_ID')
    PUSHER_KEY = os.environ.get('PUSHER_KEY')
    PUSHER_SECRET = os.environ.get('PUSHER_SECRET')
    PUSHER_CLUSTER = os.environ.get('PUSHER_CLUSTER')