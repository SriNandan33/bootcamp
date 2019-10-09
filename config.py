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