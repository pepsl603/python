from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


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
    psd = db.Column(db.String(128))
    mail = db.Column(db.String(200))
    phonenum = db.Column(db.String(20))
    recdate = db.Column(db.DateTime, default=datetime.utcnow())
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

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
