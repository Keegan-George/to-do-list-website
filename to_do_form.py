from datetime import datetime
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length
from wtforms import StringField, DateField, SubmitField


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
    submit = SubmitField(label="Add Task")
