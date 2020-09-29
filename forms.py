from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class AddForm(FlaskForm):
    title = StringField('Title: ', validators=[DataRequired()])
    description = TextAreaField('Description:', validators=[DataRequired()])
    submit = SubmitField('Add Todo')