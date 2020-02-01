from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import Form, BooleanField, StringField, PasswordField, \
    validators, TextAreaField
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description')
    image = FileField('image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
