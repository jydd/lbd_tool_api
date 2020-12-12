from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length, Optional, EqualTo
from app.models.role import Role
from app.models.user import User
import re


class UserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired('必填'), Length(1, 20)])
    nickname = StringField('昵称', validators=[DataRequired('必填'), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired('必填'), Length(6, 128, message='长度1-128个字符'), EqualTo('password2', message="必须与确认密码一致")])
    password2 = PasswordField('确认密码', validators=[DataRequired('必填'), Length(6, 128, message='长度1-128个字符')])
    role_id = SelectField('权限', validators=[DataRequired('必填')], coerce=int, choices=[(0, '选择权限')])
    cid = SelectField('区域', validators=[Optional()], coerce=int, choices=[(0, '选择县市')])

    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role_id.choices.extend([(i.id, i.nickname) for i in Role.query.all()])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户已被占用')

        if not re.match(r"^1[35678]\d{9}$", field.data):
            raise ValidationError('必须是手机号码')

    def load(self, data):
        """填充数据
        """
        for k, v in data.__dict__.items():
            if hasattr(self, k):
                self.__dict__[k].data = '' if v is None else v


class UserUpdateForm(UserForm):
    password = PasswordField('密码', validators=[Optional(), Length(6, 128, message='长度1-128个字符'), EqualTo('password2', message="必须与确认密码一致")])
    password2 = PasswordField('确认密码', validators=[Optional(), Length(6, 128, message='长度1-128个字符')])

    def load(self, data):
        """填充数据
        """
        for k, v in data.__dict__.items():
            if hasattr(self, k):
                if v is not None or v != '':
                    self.__dict__[k].data = v
