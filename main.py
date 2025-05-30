from flask import Flask, render_template, redirect, url_for
from to_do_form import ToDoForm
from os import urandom
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, ForeignKey
from datetime import datetime


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# create flask app
app = Flask(__name__)

# configure the SQLite datbase, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"

# initialize the app with the extension
db.init_app(app)

# secret key for csrf protection in flask form
app.config["SECRET_KEY"] = urandom(32)


class ToDoList(db.Model):
    __tablename__ = "todo_list_table"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column(Date, unique=True, nullable=False)
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="todo_list", cascade="all, delete-orphan"
    )


class Task(db.Model):
    __tablename__ = "task_table"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    todo_list_id: Mapped[int] = mapped_column(ForeignKey("todo_list_table.id"))
    todo_list: Mapped["ToDoList"] = relationship(back_populates="tasks")


# create table schema in database
with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    form = ToDoForm()
    todo_lists = db.session.execute(
        db.select(ToDoList).order_by(ToDoList.date)
    ).scalars()

    if form.validate_on_submit():
        date = form.date.data
        task = form.task.data

        new_task = Task(title=task)

        existing_todo_list = ToDoList.query.filter_by(date=date).first()

        if existing_todo_list:
            existing_todo_list.tasks.append(new_task)
            db.session.commit()

        else:
            new_todo_list = ToDoList(date=date)
            new_todo_list.tasks.append(new_task)
            db.session.add(new_todo_list)
            db.session.commit()
        return redirect(url_for("home"))

    return render_template("index.html", form=form, todo_lists=todo_lists)


@app.route("/delete/todo_list/<int:id>")
def delete_todo_list(id):
    list_to_delete = db.get_or_404(entity=ToDoList, ident=id)
    db.session.delete(list_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/task/<int:id>")
def delete_task(id):
    task_to_delete = db.get_or_404(entity=Task, ident=id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
