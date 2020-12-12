from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired, Length, Optional, URL, ValidationError
from app.models.netease import Netease


netease_status = {
    0: '不可用',
    1: '正常',
    2: '黑名单'
}

netease_tasks_types = {
    1: '签到',
    2: '听歌'
}

netease_tasks_status = {
    0: '未开始',
    1: '完成',
    2: '进行中',
    3: '异常'
}

class NeteaseForm(FlaskForm):
    username = StringField('账号', validators=[DataRequired('账号不能为空'), Length(1, 255)], render_kw={'placeholder': '输入账号'})
    password = StringField('密码', validators=[DataRequired('密码不能为空'), Length(1, 255)], render_kw={'placeholder': '输入密码'})
    status = SelectField('状态', validators=[Optional()], coerce=int, default=1, choices=netease_status.items())
    submit = SubmitField('提交')

    def load(self, data):
        """填充数据
        """
        for k, v in data.__dict__.items():
            if hasattr(self, k):
                self.__dict__[k].data = '' if v is None else v

    def validate_username(self, field):
        if Netease.query.filter_by(username=field.data).first():
            raise ValidationError('用户已被占用')


class NeteaseTasksForm(FlaskForm):
    types = SelectField('类型', validators=[Optional()], coerce=int, default=1, choices=netease_tasks_types.items())
    status = SelectField('状态', validators=[Optional()], coerce=int, default=0, choices=netease_tasks_status.items())
    submit = SubmitField('提交')

    def load(self, data):
        """填充数据
        """
        for k, v in data.__dict__.items():
            if hasattr(self, k):
                self.__dict__[k].data = '' if v is None else v
