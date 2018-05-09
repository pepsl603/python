from flask import Flask
from flask import render_template
# from flask import make_response
from flask import redirect
from flask_bootstrap import Bootstrap
# from flask import abort
# from flask_script import Manager, Server
import config

app = Flask(__name__)  # type:Flask
app.config.from_object(config)
bootstrap = Bootstrap(app)
# manager = Manager(app)
# manager.add_command("runserver 0.0.0.0 8001", Server(use_debugger=True))


# 起始页
@app.route('/index/<name>')
@app.route('/index/')
@app.route('/')
def start(name=''):
    return render_template('index.html', name=name)


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


# 不存在页面报错
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
