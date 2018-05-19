from datetime import datetime
from flask import render_template
from flask import url_for, flash, redirect
from . import main
from ..models import User, Role
from .forms import EditProfileForm, EditProfileAdminForm
from .. import db
from ..decorators import permission_required, admin_required
from ..models import Permission
from flask_login import login_required, current_user
# from wtforms import ValidationError
import base64
from flask import send_file, abort
import io
import requests


# 起始页
@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', currenttime=datetime.utcnow())


# 首页
@main.route('/main/<name>/')
@main.route('/main/')
def _main(name=''):
    return render_template('main.html', name=name)


# 测试页面
@main.route('/test/')
def test():
    return render_template('test.html')


# 用户资料查询页面
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user, base64=base64)


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
        except Exception as ex:
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
        except Exception as ex:
            print(ex)
            db.session.rollback()
    return send_file(io.BytesIO(user.user_pic_small), mimetype='image/png')


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
        except:
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
        except:
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


@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return render_template('main.html', message='此页面仅协管员可操作')


@main.route('/admin')
@login_required
@admin_required
def for_admin_only():
    return render_template('main.html', message="此页面仅管理员可操作")
