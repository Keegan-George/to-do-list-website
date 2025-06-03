from datetime import datetime
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length
from wtforms import StringField, DateField, BooleanField, SubmitField


class ToDoForm(FlaskForm):
    date = DateField(
        label="Date:",
        default=lambda: datetime.today().date(),
        validators=[InputRequired()],
    )
    task = StringField(
        label="Task:",
        validators=[InputRequired(), Length(max=50)],
    )
    complete = BooleanField(label="complete")
    submit = SubmitField(label="Add Task")
