from models import db, Task
from flask import Blueprint, request, redirect, url_for


update_bp = Blueprint("update", __name__)


@update_bp.route("/update-task-completion", methods=["POST"])
def update_task_completion():
    completion_states = {"True": True, "False": False}

    for task_id, complete in request.form.items():
        if complete in completion_states:
            id = int(task_id)
            task: Task = db.get_or_404(entity=Task, ident=id)
            task.is_done = completion_states[complete]

    db.session.commit()

    return redirect(url_for("home.home"))
