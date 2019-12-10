from flask_wtf import FlaskForm
from wtforms import  FileField, SubmitField, FormField, PasswordField, StringField, TextAreaField, SelectField, RadioField, FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length, Regexp


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])