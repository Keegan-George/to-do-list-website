from flask import Blueprint, request, redirect, url_for
from models import db, Task

update_bp = Blueprint("update", __name__)


@update_bp.route("/update-task-completion", methods=["POST"])
def update_task_completion():
    completion_states = {"True": True, "False": False}

    for task_id in request.form:
        id = int(task_id)
        complete = request.form[task_id]

        if complete in completion_states:
            task: Task = db.get_or_404(entity=Task, ident=id)
            task.is_done = completion_states[complete]

    db.session.commit()

    return redirect(url_for("home.home"))
