from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email


class NameForm(FlaskForm):
    name = StringField('你的名字是？', validators=[DataRequired()])
    mail = StringField('你的电子邮箱是？', validators=[DataRequired(), Email()])
    password = PasswordField('登录密码', validators=[DataRequired()])
    submit = SubmitField('提交')
