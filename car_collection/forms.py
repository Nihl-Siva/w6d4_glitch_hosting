from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField()

class CarForm(FlaskForm):
    make = StringField('Make')
    model = StringField('Model')
    year = IntegerField('Year')
    color = StringField('Color')
    submit_button = SubmitField()
