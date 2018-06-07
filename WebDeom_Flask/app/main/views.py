from datetime import datetime
from flask import render_template, current_app, abort
from flask import url_for, flash, redirect, request, make_response
from . import main
from ..models import User, Role, Post, Comment
from .forms import EditProfileForm, EditProfileAdminForm, PostForm, CommentForm
from .. import db
from ..decorators import permission_required, admin_required
from ..models import Permission
from flask_login import login_required, current_user
# from wtforms import ValidationError
import base64
from flask import send_file
from sqlalchemy.exc import DatabaseError
import io
import requests


# 起始页
@main.route('/', methods=['GET', 'POST'])
def index():
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
        if show_followed:
            query = current_user.followed_posts
        else:
            query = Post.query
        page = request.args.get('page', 1, type=int)
        pagination = query.order_by(Post.timestap.desc()).\
            paginate(page, per_page=current_app.config.get('H2D_POSTS_PER_PAGE'), error_out=False)
        posts = pagination.items
        return render_template('index.html', currenttime=datetime.utcnow(),
                           show_followed=show_followed, posts=posts, pagination=pagination)
    else:
        return render_template('index.html', currenttime=datetime.utcnow())


# 首页
@main.route('/home/', methods=['GET', 'POST'])
@login_required
def home():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        try:
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('main.home'))
        except DatabaseError:
            db.session.rollback()
            flash('提交失败')

    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestap.desc()).paginate(page,
                                                                    per_page=current_app.config.get('H2D_POSTS_PER_PAGE'),
                                                                    error_out=False)
    posts = pagination.items
    # posts = Post.query.order_by(Post.timestap.desc()).all()

    return render_template('home.html', form=form, posts=posts, pagination=pagination)


# 测试页面
@main.route('/test/')
def test():
    return render_template('test.html')


# 用户资料查询页面
@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    # posts = user.posts.order_by(Post.timestap.desc()).all()

    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestap.desc()).paginate(page,
                                                                    per_page=current_app.config.get('H2D_POSTS_PER_PAGE'),
                                                                    error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts, pagination=pagination)


@main.route('/get_pic/<int:u_id>', methods=['GET', 'POST'])
@login_required
def get_pic(u_id):
    user = User.query.get_or_404(u_id)
    if user.user_pic is None:
        pic_data = requests.get(user.gravatar(256))
        user.user_pic = pic_data.content
        try:
            db.session.add(user)
            db.session.commit()
        except DatabaseError as ex:
            print(ex)
            db.session.rollback()
    return send_file(io.BytesIO(user.user_pic), mimetype='image/png')


@main.route('/get_pic_small/<int:u_id>', methods=['GET', 'POST'])
@login_required
def get_pic_small(u_id):
    # base64.b64encode
    user = User.query.get_or_404(u_id)
    if user.user_pic_small is None:
        pic_data_small = requests.get(user.gravatar(18))
        user.user_pic_small = pic_data_small.content
        try:
            db.session.add(user)
            db.session.commit()
        except DatabaseError as ex:
            print(ex)
            db.session.rollback()
    return send_file(io.BytesIO(user.user_pic_small), mimetype='image/png')


@main.route('/get_pic_list/<int:u_id>', methods=['GET', 'POST'])
@login_required
def get_pic_list(u_id):
    # base64.b64encode
    user = User.query.get_or_404(u_id)
    if user.user_pic_40 is None:
        pic_data_40 = requests.get(user.gravatar(40))
        user.user_pic_40 = pic_data_40.content
        try:
            db.session.add(user)
            db.session.commit()
        except DatabaseError as ex:
            print(ex)
            db.session.rollback()
    return send_file(io.BytesIO(user.user_pic_40), mimetype='image/png')


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_form = EditProfileForm()
    if user_form.validate_on_submit():
        current_user.name = user_form.name.data
        current_user.location = user_form.location.data
        current_user.about_me = user_form.about_me.data
        try:
            db.session.add(current_user)
            db.session.commit()
        except DatabaseError:
            db.session.rollback()
            return render_template('', form=user_form)
        flash('资料已修改.')
        return redirect(url_for('main.user', username=current_user.username))
    user_form.name.data = current_user.name
    user_form.location.data = current_user.location
    user_form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=user_form)


@main.route('/edit-profile/<int:u_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(u_id):
    user = User.query.get_or_404(u_id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.mail = form.email.data
        user.username = form.username.data
        user.role = Role.query.get(form.role.data)
        user.confirmed = form.confirmed.data
        user.name = form.name.data
        user.phonenum = form.phonenumber.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        try:
            db.session.add(user)
            db.session.commit()
        except DatabaseError:
            db.session.rollback()
            return render_template('edit_profile.html', form=form, user=user)
        flash('资料已修改')
        return redirect(url_for('main.user', username=user.username))
    # 出错后不从数据库重新获取值填充到界面
    if len(form.errors.items()) > 0:
        return render_template('edit_profile.html', form=form, user=user)
    form.email.data = user.mail
    form.username.data = user.username
    form.role.data = user.role_id
    form.confirmed.data = user.confirmed
    form.name.data = user.name
    form.phonenumber.data = user.phonenum
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/post/<int:id>', methods=['POST', 'GET'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post=post,
                          author=current_user._get_current_object())
        try:
            db.session.add(comment)
            db.session.commit()
        except DatabaseError:
            db.session.rollback()
            flash('提交失败')
        return redirect(url_for('main.post', id=post.id, page=-1))

    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // current_app.config.get('H2D_POSTS_PER_PAGE') + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
            page, per_page=current_app.config.get('H2D_POSTS_PER_PAGE'), error_out=False
        )
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


@main.route('/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        try:
            db.session.add(post)
            db.session.commit()
        except DatabaseError:
            db.session.rollback()
        return redirect(url_for('main.post', id=post.id))
    form.body.data = post.body
    return render_template('post_edit.html', form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户名：' + username)
        return redirect(url_for('main.home'))
    if current_user.is_following(user):
        flash('你已经关注了该用户')
        return redirect(url_for('main.user', username=username))
    if not current_user.follow(user):
        flash('关注失败')
    else:
        flash('你成功关注了 %s.' % username)
    return redirect(url_for('main.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户名：' + username)
        return redirect(url_for('main.home'))
    if not current_user.is_following(user):
        flash('你还没有关注该用户')
        return redirect(url_for('main.user', username=username))
    if not current_user.unfollow(user):
        flash('取消关注失败')
    else:
        flash('你成功取消了对 %s 的关注.' % username)
    return redirect(url_for('main.user', username=username))


@main.route('/followers/<username>')
@login_required
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户名：' + username)
        return redirect(url_for('main.home'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config.get('H2D_POSTS_PER_PAGE'), error_out=False
    )
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title='粉丝',
                           endpoint='main.followers',pagination=pagination,
                           follows=follows)


@main.route('/followed_by/<username>')
@login_required
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户名：' + username)
        return redirect(url_for('main.home'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config.get('H2D_POSTS_PER_PAGE'), error_out=False
    )
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title='关注',
                           endpoint='main.followers', pagination=pagination,
                           follows=follows)


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config.get('H2D_POSTS_PER_PAGE'),error_out=False
    )
    comments = pagination.items
    return render_template('moderate.html', comments=comments, pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    try:
        db.session.add(comment)
        db.session.commit()
    except DatabaseError:
        db.session.rollback()
        flash('启用评论失败')
    return redirect(url_for('main.moderate', page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    try:
        db.session.add(comment)
        db.session.commit()
    except DatabaseError:
        db.session.rollback()
        flash('禁用评论失败')
    return redirect(url_for('main.moderate', page=request.args.get('page', 1, type=int)))


@main.route('/all')
@login_required
def show_all():
    req = make_response(redirect(url_for('main.index')))
    req.set_cookie('show_followed', '', max_age=(30*24*60*60))
    return req


@main.route('/followed')
@login_required
def show_followed():
    req = make_response(redirect(url_for('main.index')))
    req.set_cookie('show_followed', '1', max_age=(30*24*60*60))
    return req


@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return render_template('index.html', message='此页面仅协管员可操作')


@main.route('/admin')
@login_required
@admin_required
def for_admin_only():
    return render_template('index.html', message="此页面仅管理员可操作")
