from models import db, Task, ToDoList
from flask import Blueprint, redirect, url_for


delete_bp = Blueprint("delete", __name__)


@delete_bp.route("/todo_list/<int:id>")
def delete_todo_list(id):
    list_to_delete = db.get_or_404(entity=ToDoList, ident=id)
    db.session.delete(list_to_delete)
    db.session.commit()
    return redirect(url_for("home.home"))


@delete_bp.route("/task/<int:id>")
def delete_task(id):
    task_to_delete = db.get_or_404(entity=Task, ident=id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for("home.home"))
