from app import create_app, db
from app.models import User, Post


application = create_app()

@application.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Post': Post}