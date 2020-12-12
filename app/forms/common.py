from flask_wtf import FlaskForm
from wtforms import StringField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length


class AjaxDeleteForm(FlaskForm):
    ids = StringField('id', validators=[DataRequired(), Length(1, 300)])


class FileUploadForm(FlaskForm):
    upload = FileField('缩略图', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], '只允许上传图片')])
