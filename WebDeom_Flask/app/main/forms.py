from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField, SelectField
from flask_pagedown.fields import PageDownField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email, Length, Regexp
from ..models import Role, User


class NameForm(FlaskForm):
    name = StringField('你的名字是？', validators=[DataRequired()])
    mail = StringField('你的电子邮箱是？', validators=[DataRequired(), Email()])
    password = PasswordField('登录密码', validators=[DataRequired()])
    submit = SubmitField('提交')


class EditProfileForm(FlaskForm):
    name = StringField('真是姓名:', validators=[Length(0, 20)])
    location = StringField('你的住址:', validators=[Length(0, 180)])
    about_me = TextAreaField('个人简介')
    submit = SubmitField('保存')


class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱*', validators=[DataRequired(), Email('请填写正确的邮箱'), Length(1, 64)])
    username = StringField('用户名*', validators=[DataRequired(), Length(4, 20, '4-20个字符'),
                                               Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0, '4-20个字符，可包含数字、字母、下划线,首位必须为字母')])

    confirmed = BooleanField('验证状态')
    role = SelectField('角色', coerce=int)
    name = StringField('真是姓名:', validators=[Length(0, 200)])
    phonenumber = StringField('手机号码', validators=[Regexp('^((13[0-9])|(14[5,7])|(15[0-3,5-9])|'
                                                         '(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\d{8}$',
                                                         0, '请输入正确的手机号码')])
    location = StringField('你的住址:', validators=[Length(0, 180)])
    about_me = TextAreaField('个人简介')
    submit = SubmitField('保存')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in
                             Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.mail and \
                User.query.filter_by(mail=field.data).first():
            raise ValidationError('邮箱(%s)已被注册使用' % field.data)

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名(%s)已被他人使用' % field.data)


class PostForm(FlaskForm):
    # body = TextAreaField("说点什么吧。。。(支持Markdown语法）", validators=[DataRequired()])
    body = PageDownField("说点什么吧。。。", validators=[DataRequired()])
    submit = SubmitField('提交')


class CommentForm(FlaskForm):
    body = StringField('', validators=[DataRequired()])
    submit = SubmitField('提交')

