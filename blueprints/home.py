from to_do_form import ToDoForm
from models import db, Task, ToDoList
from flask import Blueprint, redirect, render_template, url_for


home_bp = Blueprint("home", __name__)


@home_bp.route("/", methods=["GET", "POST"])
def home():
    form = ToDoForm()
    todo_lists = db.session.execute(
        db.select(ToDoList).order_by(ToDoList.date)
    ).scalars()

    if form.validate_on_submit():
        date = form.date.data
        task = form.task.data

        add_task(date, task)

        return redirect(url_for("home.home"))

    return render_template("index.html", form=form, todo_lists=todo_lists)


def add_task(date, task: str) -> None:
    """
    Add Task to a To-Do List. Create a new To-Do List if one doesn't already exist.
    """
    new_task = Task(title=task)

    # query if the a todo list with that date exists
    todo_list: ToDoList = ToDoList.query.filter_by(date=date).first()

    # if the list doesn't already exist create it
    if not todo_list:
        todo_list = ToDoList(date=date)
        db.session.add(todo_list)

    todo_list.tasks.append(new_task)

    db.session.commit()
