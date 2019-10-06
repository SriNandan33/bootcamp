from datetime import datetime

from flask import (
    make_response,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for
)
from flask_login import current_user, login_required
from app import db
from app.core import bp
from app.core.forms import PostForm, EditProfileForm
from app.models import User, Post

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post is now live!", "success")
        return redirect(url_for('core.index'))
    posts = current_user.feed().paginate(page, current_app.config["POSTS_PER_PAGE"], False)
    prev_url = url_for('core.index', page=posts.prev_num)\
        if posts.has_prev else None
    next_url = url_for('core.index', page=posts.next_num)\
        if posts.has_next else None
    return render_template('index.html', title="Feed", posts=posts.items, form=form,\
        prev_url=prev_url, next_url=next_url)

@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config["POSTS_PER_PAGE"], False
    )
    prev_url = url_for('core.explore', page=posts.prev_num)\
        if posts.has_prev else None
    next_url = url_for('core.explore', page=posts.next_num)\
        if posts.has_next else None
    return render_template('index.html', title="Explore", posts=posts.items, \
        prev_url=prev_url, next_url=next_url)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config["POSTS_PER_PAGE"], False
    )
    prev_url = url_for('core.user', username=username, page=posts.prev_num)\
        if posts.has_prev else None
    next_url = url_for('core.user', username=username, page=posts.next_num)\
        if posts.has_next else None
    return render_template('user.html', user=user, posts=posts.items, \
        prev_url=prev_url, next_url=next_url)

@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_popup.html', user=user)

@bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.bio.data
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('core.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.bio.data = current_user.about_me   
    return render_template('edit_profile.html', form=form, title="Edit Profile")


def ajax_flash(msg_type, message, message_list):
    message_list.append({
        'type': msg_type,
        'message': message
    })
    return message_list


@bp.route('/follow/<username>')
def follow(username):
    flash_messages = []

    data = {
        'redirect': ''
    }

    user = User.query.filter_by(username=username).first()

    if not user:
        flash_messages = ajax_flash('info', 'User not found', flash_messages)
    elif user == current_user:
        flash_messages = ajax_flash('info', 'You can\'t follow yourself!', flash_messages)
    else:
        current_user.follow(user)
        db.session.commit()
        flash_messages = ajax_flash('success', f'You are following {username}', flash_messages)

    data['flash_messages'] = flash_messages

    r = make_response(data)
    r.mimetype = 'application/json'
    return r


@bp.route('/unfollow/<username>')
def unfollow(username):
    flash_messages = [];

    data = {
        'redirect': ''
    }
    user = User.query.filter_by(username=username).first()
    if not user:
        flash_messages = ajax_flash('info', 'User not found', flash_messages)
        data['redirect'] = url_for('core.index')
    elif user == current_user:
        flash_messages = ajax_flash('info', 'You can\'t unfollow yourself', flash_messages)
    else:
        current_user.unfollow(user)
        db.session.commit()
        flash_messages = ajax_flash('success', f'You unfollowed {username}', flash_messages)

    data['flash_messages'] = flash_messages

    r = make_response(data)
    r.mimetype = 'application/json'
    return r