import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 为了实现 CSRF 保护， Flask-WTF 需要程序设置一个密钥。 Flask-WTF 使用这个密钥生成
    # 加密令牌，再用令牌验证请求中表单数据的真伪
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # 将会追踪对象的修改并且发送信号。这需要额外的内存
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 邮箱
    H2D_MAIL_SUBJECT_PREFIX = '[H2D]'
    H2D_MAIL_SENDER = 'H2D Admin <product@hangar.cn>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # 邮箱
    MAIL_SERVER = 'smtp.ym.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # 数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite3')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                            'sqlite:///' + os.path.join(basedir, 'data-test.sqlite3')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                            'sqlite:///' + os.path.join(basedir, 'data.sqlite3')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
