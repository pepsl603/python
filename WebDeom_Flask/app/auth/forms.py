from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, InputRequired
# http://wtforms.readthedocs.io/en/stable/validators.html


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email(), Length(1, 60)])
    password = PasswordField('密码', validators=[InputRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')
