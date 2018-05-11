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
# from flask import abort
# from flask_script import Manager, Server
import config

app = Flask(__name__)  # type:Flask
app.config.from_object(config)
bootstrap = Bootstrap(app)
moment = Moment(app)
# manager = Manager(app)
# manager.add_command("runserver 0.0.0.0 8001", Server(use_debugger=True))


class NameForm(FlaskForm):
    name = StringField('你的注册邮箱是？', validators=[DataRequired(), Email()])
    psd = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('提交')


# 起始页
# @app.route('/index/<name>')
# @app.route('/index/')
@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('你切换了登录账户！')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), currenttime=datetime.utcnow())


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
@app.route('/user')
def user():
    return render_template('user.html')


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
    # manager.run()
