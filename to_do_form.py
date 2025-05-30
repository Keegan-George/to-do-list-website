from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import InputRequired
from datetime import datetime


class ToDoForm(FlaskForm):
    date = DateField(
        label="Date:", default=datetime.today(), validators=[InputRequired()]
    )
    task = StringField(label="Task:", validators=[InputRequired()])
    submit = SubmitField()
