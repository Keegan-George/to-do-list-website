from datetime import date
from models import db, Task, ToDoList


def add_task(date: date, task: str) -> None:
    """
    Add task to an existing To-Do list.
    Creates a new To-Do list if needed.
    """
    # check if a to-do list with the provided date exists
    todo_list: ToDoList = ToDoList.query.filter_by(date=date).first_or_404()

    # create a new to-do list if needed
    if not todo_list:
        todo_list = ToDoList(date=date)
        db.session.add(todo_list)

    new_task = Task(title=task, is_done=False)
    todo_list.tasks.append(new_task)

    db.session.commit()
