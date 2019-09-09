from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'srinivas'}
    posts = [
        {
            'author': {'username': 'Nandu'},
            'body': 'This post is written by Nandu'
        },
        {
            'author': {'username': 'Srinivas'},
            'body': 'This post is writeen by Srinivas'
        }
    ]
    return render_template('index.html', user=user, posts=posts)