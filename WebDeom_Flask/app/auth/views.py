from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .forms import LoginForm
from .forms import RegisterForm
from .forms import ChangePsdForm
from .forms import ResetPsdRequestForm, ResetPsdForm
from .. import db
from ..email import send_email


@auth.before_app_request
def before_request():
    """
    如果为验证，则跳转到未验证的引导页
    :return:
    """
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


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


@auth.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = User(mail=register_form.email.data,
                    username=register_form.username.data,
                    password=register_form.password.data,
                    phonenum=register_form.phonenumber.data)
        try:
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email(user.mail, '注册账号确认', 'auth/email/confirm', user=user, token=token)
            flash('发送了一封确认邮件到你的注册邮箱，请登录邮箱确认！')
        except Exception as ex:
            db.session.rollback()
            print(ex)
            flash('提交失败，请重新填写提交')
            return render_template('auth/register.html', form=register_form)
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=register_form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("你退出了登录")
    return redirect(url_for("auth.login"))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('你已经成功验证了账号，可正常使用')
    else:
        flash('验证链接无效或者已过期')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.mail, '注册账号确认', 'auth/email/confirm', user=current_user, token=token)
    flash('发送了一封新的确认邮件到你的注册邮箱，请登录邮箱确认！')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/changepsd', methods=['GET', 'POST'])
@login_required
def change_psd():
    changepsd_form = ChangePsdForm()
    if changepsd_form.validate_on_submit():
        if current_user.verify_password(changepsd_form.old_psd.data):
            current_user.password = changepsd_form.new_psd.data
            try:
                db.session.add(current_user)
                db.session.commit()
                flash('你的密码已经修改成功')
                return redirect(url_for('main.index'))
            except:
                db.session.rollback()
                flash('修改密码失败.')
        else:
            flash('原密码错误.')
    return render_template('auth/changepsd.html', form=changepsd_form)


@auth.route('/resetpsd', methods=['GET', 'POST'])
def reset_psd_queuest():
    resetpsd_request_form = ResetPsdRequestForm()
    if resetpsd_request_form.validate_on_submit():
        user = User.query.filter_by(mail=resetpsd_request_form.email.data).first()
        if user is not None:
            token = user.generate_reset_psd_token()
            send_email(user.mail, '重置密码', 'auth/email/reset', user=user, token=token)
            flash('发送了一封重置密码的邮件到你的注册邮箱，请登录邮箱操作！')
            return redirect(url_for('auth.login'))
    return render_template('auth/resetpsd.html', form=resetpsd_request_form)


@auth.route('/resetpsd/<token>', methods=['GET', 'POST'])
def reset_psd(token):
    resetpsd_form = ResetPsdForm()
    if resetpsd_form.validate_on_submit():
        if User.reset_psd(token, resetpsd_form.new_psd.data):
            flash('密码重置成功')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/resetpsd.html', form=resetpsd_form)
