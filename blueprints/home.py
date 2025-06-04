from helper import add_task
from to_do_form import ToDoForm
from models import db, ToDoList
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
