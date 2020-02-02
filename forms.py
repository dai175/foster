from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import Form, BooleanField, StringField, PasswordField, \
    validators, TextAreaField, FieldList, FormField, SelectField
from wtforms.validators import InputRequired, InputRequired


class CategoryForm(FlaskForm):
    name = StringField('name', validators=[InputRequired()])
    description = StringField('description')
    image = FileField('image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])


class TypeForm(FlaskForm):
    category = SelectField('category', coerce=int, default=int,
                           validators=[InputRequired()])
    name = StringField('name', validators=[InputRequired()])
    description = StringField('description')
    image = FileField('image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
