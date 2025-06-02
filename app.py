from extensions import db
from os import getenv
from dotenv import load_dotenv
from to_do_form import ToDoForm
from models import ToDoList, Task
from flask import Flask, render_template, redirect, url_for
from blueprints.delete import delete_bp


def create_app():
    # create flask app
    app = Flask(__name__)

    # configure the SQLite database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL", "sqlite:///todo.db")

    # initialize the app with the extension
    db.init_app(app)

    # set secret key
    load_dotenv()
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")

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

            add_task(date, task)

            return redirect(url_for("home"))

        return render_template("index.html", form=form, todo_lists=todo_lists)

    def add_task(date, task):
        """
        Add Task to a To-Do List. Creates a new To-Do List if one doesn't already exist.
        """
        date = date
        task = task

        new_task = Task(title=task)

        existing_todo_list: ToDoList = ToDoList.query.filter_by(date=date).first()

        if existing_todo_list:
            existing_todo_list.tasks.append(new_task)

        else:
            new_todo_list = ToDoList(date=date)
            new_todo_list.tasks.append(new_task)
            db.session.add(new_todo_list)

        db.session.commit()

    app.register_blueprint(delete_bp, url_prefix="/delete")

    return app
