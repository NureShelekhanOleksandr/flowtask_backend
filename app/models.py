from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base


class TaskStatus(str, enum.Enum):
    TODO = "To do"
    IN_PROGRESS = "In progress"
    DONE = "Done"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks_created = relationship(
        "Task", foreign_keys="[Task.created_by_id]", back_populates="creator"
    )
    tasks_assigned = relationship(
        "Task", foreign_keys="[Task.assigned_user_id]", back_populates="assignee"
    )
    comments = relationship("Comment", back_populates="user")
    task_history = relationship("TaskHistory", back_populates="user")


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), nullable=False)
    deadline = Column(DateTime)
    assigned_user_id = Column(Integer, ForeignKey("users.id"))
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    attachment_url = Column(String(500))

    __table_args__ = (
        CheckConstraint(
            "status IN ('To do', 'In progress', 'Done')", name="check_status_values"
        ),
    )

    assignee = relationship(
        "User", foreign_keys=[assigned_user_id], back_populates="tasks_assigned"
    )
    creator = relationship(
        "User", foreign_keys=[created_by_id], back_populates="tasks_created"
    )
    comments = relationship("Comment", back_populates="task")
    history = relationship("TaskHistory", back_populates="task")


class TaskHistory(Base):
    __tablename__ = "task_history"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    change_type = Column(String(100), nullable=False)
    change_description = Column(Text)
    changed_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="history")
    user = relationship("User", back_populates="task_history")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="comments")
    user = relationship("User", back_populates="comments")
