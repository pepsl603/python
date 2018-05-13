from datetime import datetime
from flask import render_template, session, redirect, url_for, flash

from . import main
from .forms import NameForm
from ..models import User
from .. import db
from ..email import send_email


# 起始页
# @app.route('/index/<name>')
# @app.route('/index/')
@main.route('/', methods=['GET', 'POST'])
def index():
    # name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('你切换了登录账户！')
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data, mail=form.mail.data, password=form.password.data)
            db.session.add(user)
            session['known'] = False
            # 注册用户 发一封邮件
            if form.mail.data:
                user.recdate = datetime.utcnow()
                send_email(form.mail.data, '新用户注册', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main.index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False), currenttime=datetime.utcnow())


# 首页
@main.route('/main/<name>/')
@main.route('/main/')
def _main(name=''):
    # if name == 'q':
    #     abort(404)
    # return 'Hello %s, Flask is very very good!' % name
    # user_dict = {"1": "壹", "2": "贰"}
    # user_list = ["零", "壹", "贰", "叁"]
    # html_str = '<p>Hello </p>'
    return render_template('main.html', name=name)


# 测试页面
@main.route('/test/')
def test():
    return render_template('test.html')


# 用户管理页面
@main.route('/user')
def user():
    return render_template('404.html')
