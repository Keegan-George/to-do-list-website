from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, ForeignKey
from extensions import db


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
