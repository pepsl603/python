from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


# 关注用户               0b00000001（ 0x01） 关注其他用户
# 在他人的文章中发表评论   0b00000010（ 0x02） 在他人撰写的文章中发布评论
# 写文章                0b00000100（ 0x04） 写原创文章
# 管理他人发表的评论      0b00001000（ 0x08） 查处他人发表的不当评论
# 管理员权限             0b10000000（ 0x80） 管理网站
class Permission:
    FOLLOW = 0x01
    COMMENT = 0X02
    WRITE_ARTICLES = 0X04
    MODERATE_COMMENTS = 0X08
    ADMINISTER = 0X80


# 匿名        0b00000000（ 0x00） 未登录的用户。在程序中只有阅读权限
# 用户User    0b00000111（ 0x07） 具有发布文章、发表评论和关注其他用户的权限。这是新用户的默认角色
# 协管员   0b00001111（ 0x0f） 增加审查不当评论的权限
# 管理员   0b11111111（ 0xff） 具有所有权限，包括修改其他用户所属角色的权限
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    # 是否默认角色
    default = db.Column(db.Boolean, default=False)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

    # 初始化角色数据
    @staticmethod
    def insert_roles():
        roles = {
            '普通用户': (Permission.FOLLOW | Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            '协管员': (Permission.FOLLOW | Permission.COMMENT |
                    Permission.WRITE_ARTICLES | Permission.MODERATE_COMMENTS, False),
            '系统管理员': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class User(UserMixin, db.Model):
    # 初始化用户角色
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.mail == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='系统管理员').first()
            else:
                self.role = Role.query.filter_by(default=True).first()

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, index=True)
    psd = db.Column(db.String(128))
    mail = db.Column(db.String(200))
    phonenum = db.Column(db.String(20))
    recdate = db.Column(db.DateTime, default=datetime.utcnow())
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)

    # 初始化用户确认token
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
            if data.get('confirm') != self.id:
                return False
        except:
            return False

        try:
            self.confirmed = True
            db.session.add(self)
            db.session.commit()
        except:
            self.confirmed = False
            db.session.rollback()
            return False
        return True

    def generate_reset_psd_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_psd(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
            user = User.query.get(data.get('reset'))
            if user is None:
                return False
        except:
            return False

        try:
            user.password = new_password
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            return False
        return True


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.psd = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.psd, password)

    def __repr__(self):
        return '<User %r>' % self.username

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


# 未登陆用户，统一可通过current_user调用can，is_administrator 方法
login_manager.anonymous_user = AnonymousUser


# 加载用户的回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
