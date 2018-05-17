from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email, Length, InputRequired, EqualTo, Regexp
# http://wtforms.readthedocs.io/en/stable/validators.html
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email('请填写正确的邮箱'), Length(1, 64)])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    email = StringField('邮箱*', validators=[DataRequired(), Email('请填写正确的邮箱'), Length(1, 64)])
    username = StringField('用户名*', validators=[DataRequired(), Length(4, 20, '4-20个字符'),
                                               Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0, '4-20个字符，可包含数字、字母、下划线,首位必须为字母')])
    # ^开始  $结束
    password = PasswordField('密码*', validators=[DataRequired(), EqualTo('password2', message='两次输入密码要保持一致')])
    password2 = PasswordField('再次确认*', validators=[InputRequired()])
    phonenumber = StringField('手机号码')
    submit = SubmitField('提交')

    def validate_email(self, field):
        if User.query.filter_by(mail=field.data).first():
            raise ValidationError('该邮箱已经被注册使用.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已经被注册使用.')


class ChangePsdForm(FlaskForm):
    old_psd = PasswordField('旧密码*', validators=[DataRequired()])
    new_psd = PasswordField('新密码*', validators=[DataRequired(), EqualTo('new_psd2', message='两次输入密码要保持一致')])
    new_psd2 = PasswordField('再次确认*', validators=[DataRequired()])
    submit = SubmitField('提交')


class ResetPsdRequestForm(FlaskForm):
    email = StringField('注册邮箱', validators=[DataRequired(), Email('请填写正确的邮箱'), Length(1, 64)])
    submit = SubmitField('提交')


class ResetPsdForm(FlaskForm):
    new_psd = PasswordField('新密码*', validators=[DataRequired(), EqualTo('new_psd2', message='两次输入密码要保持一致')])
    new_psd2 = PasswordField('再次确认*', validators=[DataRequired()])
    submit = SubmitField('提交')
