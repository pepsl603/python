# encoding:utf-8

DEBUG = True

# 若要启动生产环境，则要先设置环境变量FLASK_ENV=PRODUCTION：
ENV = 'development'

# 为了实现 CSRF 保护， Flask-WTF 需要程序设置一个密钥。 Flask-WTF 使用这个密钥生成
# 加密令牌，再用令牌验证请求中表单数据的真伪
SECRET_KEY = 'hard to guess string'
