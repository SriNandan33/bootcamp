from flask import render_template, flash, redirect, url_for

from app import app
from app.forms import LoginForm

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

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for the user {}, rember me'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title="Sign In", form=form)