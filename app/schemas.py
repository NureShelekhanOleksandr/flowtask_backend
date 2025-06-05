from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    deadline: Optional[datetime] = None
    assigned_user_id: Optional[int] = None
    attachment_url: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskOut(TaskBase):
    id: int
    created_by_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    task_id: int


class CommentOut(CommentBase):
    id: int
    task_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TaskHistoryBase(BaseModel):
    change_type: str
    change_description: str


class TaskHistoryCreate(TaskHistoryBase):
    task_id: int


class TaskHistoryOut(TaskHistoryBase):
    id: int
    task_id: int
    user_id: int
    changed_at: datetime

    class Config:
        from_attributes = True
