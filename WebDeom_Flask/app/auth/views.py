from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(mail=login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('登录失败，不正确的用户名或者密码')
    return render_template('auth/login.html', form=login_form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("你退出了登录")
    return redirect(url_for("auth.login"))

