from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreateRequest, TaskResponse, TaskUpdateRequest, AssignTaskRequest
from app.models.user import User
from app.models.task import Task
from app.models.project import Project
from app.dependencies import get_current_user
from app.database import get_db
from uuid import UUID
from typing import List
import logging
from datetime import datetime, timezone
from app.services.notification_service import publish_task_assignment

router = APIRouter()

@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    data: TaskCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = (
        db.query(Project).filter(
            Project.id == data.project_id,
            Project.owner_id == current_user.id
        ).first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="project do not exists"
        )
    
    if data.assigned_to is not None:
        assigned_user = (
            db.query(User)
            .filter(User.id == data.assigned_to)
            .first()
        )

        if assigned_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assigned user not found"
            )
    
    task = Task(
        project_id=data.project_id,
        title=data.title,
        description=data.description,
        status=data.status,
        priority=data.priority,
        assigned_to=data.assigned_to,
        created_by=current_user.id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tasks = (
        db.query(Task)
        .join(Project, Task.project_id == Project.id)
        .filter(Project.owner_id == current_user.id)
        .all()
    )

    return tasks

@router.get("/tasks/{id}", response_model=TaskResponse)
def get_task(
    id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = db.get(Task, id)

    if task is None:
        raise HTTPException(404, "Task not found")

    project = (
        db.query(Project)
        .filter(
            Project.id == task.project_id,
            Project.owner_id == current_user.id,
        )
        .first()
    )

    if project is None:
        raise HTTPException(403, "Project not found")

    return task

@router.put("/tasks/{id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(
    id: UUID,
    data: TaskUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = (
        db.query(Task).filter(
            Task.id == id
        ).first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
    )

    project = (
        db.query(Project).filter(
            Project.id == task.project_id,
            Project.owner_id == current_user.id
        ).first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project not found"
        )
    
    if data.title is not None:
        task.title = data.title

    if data.description is not None:
        task.description = data.description

    if data.status is not None:
        task.status = data.status

    if data.priority is not None:
        task.priority = data.priority

    db.commit()
    db.refresh(task)

    return task

logger = logging.getLogger(__name__)

@router.patch("/tasks/{id}/assign", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def assign_task(
    id: UUID,
    data: AssignTaskRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    task = db.get(Task, id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    assignee = db.get(User, data.assigned_to)

    if not assignee:
        raise HTTPException(
            status_code=404,
            detail="Assigned user not found"
        )
    
    task.assigned_to = assignee.id
    task.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(task)

    # Service Bus notification
    message = {
        "task_id": str(task.id),
        "task_title": task.title,
        "project_id": str(task.project_id),
        "assigned_to": assignee.email,
        "assigned_by": current_user.email,
        "priority": task.priority,
        "assigned_at": datetime.now(timezone.utc).isoformat()
    }

    try:
        publish_task_assignment(message)

    except Exception as ex:
        logger.warning(
            "Task assigned but Service Bus publish failed: %s",
            ex,
            exc_info=True
        )

    return task

@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = (
        db.query(Task).filter(
            Task.id == id
        ).first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
    )

    project = (
        db.query(Project).filter(
            Project.id == task.project_id,
            Project.owner_id == current_user.id
        ).first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project not found"
        )
    
    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }