from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, url_for
import hashlib
import requests
import bleach
from markdown import markdown
from sqlalchemy.exc import DatabaseError
from app.exceptions import ValidationError


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


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


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
        if self.mail is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.mail.encode('utf-8')).hexdigest()
        # print(datetime.now())
        if self.mail is not None and self.user_pic is None:
            pic_data = requests.get(self.gravatar(256))
            self.user_pic = pic_data.content
        if self.mail is not None and self.user_pic_small is None:
            pic_data_small = requests.get(self.gravatar(18))
            self.user_pic_small = pic_data_small.content
        if self.mail is not None and self.user_pic_40 is None:
            pic_data_40 = requests.get(self.gravatar(40))
            self.user_pic_40 = pic_data_40.content
        # print(datetime.now())

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, index=True)
    psd = db.Column(db.String(128))
    mail = db.Column(db.String(200))
    phonenum = db.Column(db.String(20))
    recdate = db.Column(db.DateTime(), default=datetime.utcnow)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(40))
    location = db.Column(db.String(200))
    about_me = db.Column(db.Text())
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    user_pic = db.Column(db.LargeBinary())
    user_pic_small = db.Column(db.LargeBinary())
    user_pic_40 = db.Column(db.LargeBinary())
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    followed = db.relationship('Follow', foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')

    followers = db.relationship("Follow", foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')


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
        except DatabaseError:
            self.confirmed = False
            db.session.rollback()
            return False
        return True

    def generate_reset_psd_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return None
        return User.query.get(data.get('id'))


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
        except DatabaseError:
            db.session.rollback()
            return False
        return True

    @property
    def followed_posts(self):
        return Post.query.join(Follow, Follow.followed_id == Post.author_id)\
            .filter(Follow.follower_id == self.id)

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

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        try:
            db.session.commit()
        except:
            db.session.remove()

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = "https://secure.gravatar.com/avatar"
        else:
            url = "http://www.gravatar.com/avatar"
        hash = self.avatar_hash or hashlib.md5(self.mail.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating
        )

    def is_following(self, user):
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)
            try:
                db.session.commit()
            except DatabaseError:
                db.session.rollback()
                return False
        return True

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)
            try:
                db.session.commit()
            except DatabaseError:
                db.session.rollback()
                return False
        return True

    def to_json(self):
        josn_user = {
            'url': url_for('api.get_user', id=self.id, _external=True),
            'usename': self.username,
            'member_since': self.recdate,
            'lats_seen': self.last_seen,
            'posts_url': url_for('api.get_user_posts', id=self.id, _external=True),
            'followed_posts_url': url_for('api.get_user_followed_posts', id=self.id, _external=True),
            'post_count': self.posts.count()
        }
        return josn_user

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(mail=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(),
                     psd=forgery_py.lorem_ipsum.word(),
                     confirmed=True,
                     name=forgery_py.name.full_name(),
                     location=forgery_py.address.city(),
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     recdate=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestap = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body_html = db.Column(db.Text)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestap,
            'author_url': url_for('api.get_user', id=self.author_id, _external=True),
            'comments_url': url_for('api.get_post_comments', id=self.id, _external=True),
            'comment_count': self.comments.count()
        }
        return json_post

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'br',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),
                                                       tags=allowed_tags, strip=True))
    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('post does not have a body.')
        return Post(body=body)

    @staticmethod
    def generate_fake(count=100):
        from random import randint, seed
        import forgery_py
        from sqlalchemy.exc import DatabaseError

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                     timestap=forgery_py.date.date(True),
                     author=u)
            db.session.add(u)
            try:
                db.session.commit()
            except DatabaseError:
                db.session.rollback()


db.event.listen(Post.body, 'set', Post.on_changed_body)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def to_json(self):
        json_comment = {
            'url': url_for('api.get_comment', id=self.id, _external=True),
            'post_url': url_for('api.get_post', id=self.post_id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author_url': url_for('api.get_user', id=self.author_id, _external=True)
        }
        return json_comment

    @staticmethod
    def from_json(json_comment):
        body = json_comment.get('body')
        if body is None or body == '':
            raise ValidationError('comments does no have a body.')
        return Comment(body=body)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(Comment.body, 'set', Comment.on_changed_body)


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
