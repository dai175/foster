from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import DataRequired


class CategoryForm(Form):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description')
    image = StringField('image')
