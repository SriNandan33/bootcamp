from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, \
    PostForm
from app.models import User, Post

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post is now live!")
        return redirect(url_for('index'))
    posts = current_user.feed().paginate(page, app.config["POSTS_PER_PAGE"], False)
    prev_url = url_for('index', page=posts.prev_num)\
        if posts.has_prev else None
    next_url = url_for('index', page=posts.next_num)\
        if posts.has_next else None
    return render_template('index.html', title="Feed", posts=posts.items, form=form,\
        prev_url=prev_url, next_url=next_url)

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config["POSTS_PER_PAGE"], False
    )
    prev_url = url_for('explore', page=posts.prev_num)\
        if posts.has_prev else None
    next_url = url_for('explore', page=posts.next_num)\
        if posts.has_next else None
    return render_template('index.html', title="Explore", posts=posts.items, \
        prev_url=prev_url, next_url=next_url)

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        flash('Login successful!')
        return redirect(next_page)
    return render_template('login.html', title="Sign In", form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Successfully registered. Please login to continue')
        return redirect(url_for('login'))
    return render_template('register.html', title="Sign Up", form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config["POSTS_PER_PAGE"], False
    )
    prev_url = url_for('user', username=username, page=posts.prev_num)\
        if posts.has_prev else None
    next_url = url_for('user', username=username, page=posts.next_num)\
        if posts.has_next else None
    return render_template('user.html', user=user, posts=posts.items, \
        prev_url=prev_url, next_url=next_url)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.bio.data
        db.session.commit()
        flash("Profile updated successfully!")
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.bio.data = current_user.about_me   
    return render_template('edit_profile.html', form=form, title="Edit Profile")


@app.route('/follow/<username>')
def follow(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User not found")
        return redirect(url_for("index"))
    if user == current_user:
        flash("You can't follow yourself")
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(f"You are following {username}!")
    return redirect(url_for("user", username=username))

@app.route('/unfollow/<username>')
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User not found")
        return redirect(url_for("index"))
    if user == current_user:
        flash("You can unfollow yourself")
        return redirect(url_for("user", username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(f"You unfollowed {username}")
    return redirect(url_for('user', username=username))