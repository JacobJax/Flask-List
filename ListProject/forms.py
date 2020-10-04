import email_validator
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from ListProject.models import User

class AddForm(FlaskForm):
    title = StringField('Title: ', validators=[DataRequired()])
    description = TextAreaField('Description:', validators=[DataRequired()])
    submit = SubmitField('Add Todo')

class RegistrationForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    pass_conf = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('That email has already been registered')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('That username is already taken')


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')