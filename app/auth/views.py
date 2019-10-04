import json
import os
import string
from random import choice

import requests
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import db
from app.auth import bp
from app.auth.email import send_password_reset_email
from app.auth.forms import (LoginForm, PasswordResetRequestForm,
                            RegistrationForm, ResetPasswordForm)
from app.models import User


@bp.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('core.index')
        flash('Login successful!')
        return redirect(next_page)
    return render_template(
        'auth/login.html',
        title="Sign In",
        form=form,
        # NOTE: Necessary for facebook login flux
        app_id=os.getenv('FACEBOOK_APP_ID'))


@bp.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Successfully registered. Please login to continue')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title="Sign Up", form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Check your email for the instructions to reset your password")
        return redirect(url_for('auth.login'))
    return render_template(
        'auth/reset_password_request.html',
        title="Reset Password", form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('core.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset.")
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@bp.route('/facebook_login', methods=['POST'])
def facebook_login():
    access_token = request.form.get('access_token')
    response = requests.get(
        "https://graph.facebook.com/"
        f"v4.0/me?fields=id%2Cname%2Cemail&access_token={access_token}"
    )
    content = json.loads(response.content)
    if not (
            content.get('id') or
            content.get('email') or
            content.get('name')):
        flash('Something went wrong with facebook login. Try again.')
        return redirect(url_for('core.index'))
    user_by_facebook_id = User.query.filter_by(
        facebook_id=content['id']).first()
    user_by_email = User.query.filter_by(
        email=content['email']).first()
    user_by_username = User.query.filter_by(
        username=content['email']).first()
    if user_by_facebook_id:
        login_user(user_by_facebook_id, remember=True)
    elif user_by_email:
        user_by_email.facebook_id = content['id']
        db.session.add(user_by_email)
        db.session.commit()
        login_user(user_by_email, remember=True)
    elif user_by_username:
        flash(
            'Other user is using your facebook email as username. '
            'Try to register to our website without facebook')
        return redirect(url_for('core.index'))
    else:
        user = User(username=content['email'], email=content['email'])
        user.set_password(
            ''.join(
                choice(string.ascii_letters + string.digits)
                for _
                in range(12)
            )
        )
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
    return redirect(url_for('core.index'))
