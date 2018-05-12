from flask import Flask
from flask import render_template
# from flask import make_response
from flask import redirect, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
# from flask import abort
from flask_script import Manager, Shell, Server
import config
import os
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message
from threading import Thread
# import uuid


app = Flask(__name__)  # type:Flask
app.config.from_object(config)
bootstrap = Bootstrap(app)
moment = Moment(app)
# SQLALCHEMY_DATABASE_URI
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite3')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 将会追踪对象的修改并且发送信号。这需要额外的内存
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager = Manager(app)
manager.add_command("shell", Shell(make_context=make_shell_context))
# manager.add_command("runserver 0.0.0.0 8002", Server(use_debugger=True))
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# 邮箱发送配置
# app.config['MAIL_SERVER'] = 'smtp.ym.163.com'
# app.config['MAIL_PORT'] = 25
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
mail = Mail(app)


def send_async_email(app, msg):
    with app.app_context():
        # print(app.config['MAIL_USERNAME'])
        # print(app.config['MAIL_PASSWORD'])
        # print(app.config['H2D_MAIL_SENDER'])
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['H2D_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['H2D_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # print(to)
    # mail.send(msg)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


class NameForm(FlaskForm):
    name = StringField('你的名字是？', validators=[DataRequired()])
    mail = StringField('你的电子邮箱是？', validators=[DataRequired(), Email()])
    psd = PasswordField('登录密码', validators=[DataRequired()])
    submit = SubmitField('提交')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


# admin_role = Role(name='管理员')
# db.session.add(admin_role)
# db.session.commit()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, index=True)
    psd = db.Column(db.String(40))
    mail = db.Column(db.String(200))
    recdate = db.Column(db.DateTime, default=datetime.utcnow())
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


# 起始页
# @app.route('/index/<name>')
# @app.route('/index/')
@app.route('/', methods=['GET', 'POST'])
def index():
    # name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('你切换了登录账户！')
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data, mail=form.mail.data, psd=form.psd.data)
            db.session.add(user)
            session['known'] = False
            # 注册用户 发一封邮件
            if form.mail.data:
                send_email(form.mail.data, '新用户注册', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False), currenttime=datetime.utcnow())


# 首页
@app.route('/main/<name>/')
@app.route('/main/')
def main(name=''):
    # if name == 'q':
    #     abort(404)
    # return 'Hello %s, Flask is very very good!' % name
    # user_dict = {"1": "壹", "2": "贰"}
    # user_list = ["零", "壹", "贰", "叁"]
    # html_str = '<p>Hello </p>'
    return render_template('main.html', name=name)


# 测试页面
@app.route('/test')
def test():
    return render_template('test.html')


# 用户管理页面
# @app.route('/user')
# def user():
#     return render_template('user.html')


# 不存在页面报错截获
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# 错误页面截获
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


@app.route('/bd')
def go_bd():
    return redirect('http://www.baidu.com')


# @app.route('/')
# def hello_world():
#     response = make_response('<h1>Hello Flask ! Create a cookie!</>')
#     response.set_cookie('answer', '42')
#     return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
    manager.run()
