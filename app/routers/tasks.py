from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from .. import schemas, models, database, auth

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    task_data = task.dict()
    # Convert status enum to string value
    if isinstance(task_data["status"], models.TaskStatus):
        task_data["status"] = task_data["status"].value

    # Set the creator
    task_data["created_by_id"] = current_user.id

    db_task = models.Task(**task_data)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/", response_model=List[schemas.TaskOut])
def get_tasks(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    assigned_to: Optional[int] = None,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    query = db.query(models.Task)

    if status:
        query = query.filter(models.Task.status == status)
    if assigned_to:
        query = query.filter(models.Task.assigned_user_id == assigned_to)

    tasks = (
        query.order_by(models.Task.created_at.desc()).offset(skip).limit(limit).all()
    )
    return tasks


@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    task_update: schemas.TaskCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    for key, value in task_update.dict().items():
        if key != "created_by_id":  # Don't allow changing the creator
            setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    db.delete(db_task)
    db.commit()
    return None
