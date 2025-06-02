from datetime import date
from models import db, Task, ToDoList


def add_task(date: date, task: str) -> None:
    """
    Add Task to a To-Do List. Creates a new To-Do List if one doesn't already exist.
    """
    new_task = Task(title=task, complete=False)

    # check if a to-do list with that date exists
    todo_list: ToDoList = ToDoList.query.filter_by(date=date).first()

    # create to-do list if it does not exist
    if not todo_list:
        todo_list = ToDoList(date=date)
        db.session.add(todo_list)

    todo_list.tasks.append(new_task)

    db.session.commit()
