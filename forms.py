from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import Form, BooleanField, StringField, PasswordField, \
    validators, TextAreaField, FieldList, FormField, SelectField, FloatField
from wtforms.fields.html5 import DateField
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


class AnimalForm(FlaskForm):
    sex_list = [('1', 'male'), ('2', 'female')]

    type = SelectField('type', coerce=int, default=int,
                       validators=[InputRequired()])
    name = StringField('name', validators=[InputRequired()])
    sex = SelectField('sex', choices=sex_list, default=int,
                      validators=[InputRequired()])
    date_of_birth = DateField('date_of_birth')
    weight = FloatField('weight')
    place_of_birth = StringField('place_of_birth')
    description = StringField('description')
    image = FileField('image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
