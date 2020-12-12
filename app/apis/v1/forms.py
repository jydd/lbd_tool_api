from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Optional
from flask_wtf.file import FileField, FileRequired, FileAllowed


class BaseForm(FlaskForm):
    class Meta:
        csrf = False


class FileUploadForm(BaseForm):
    upload = FileField('图片', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'], '只允许上传图片')])


# 验证码
class CodeForm(BaseForm):
    tel = StringField('手机号', validators=[DataRequired('必填'), Length(1, 20)])
    template = StringField('模板', validators=[Optional(), Length(1, 20)])
