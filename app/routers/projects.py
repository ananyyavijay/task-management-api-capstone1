from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.project import ProjectRequest, ProjectResponse, ProjectUpdateRequest
from app.database import get_db
from app.models.user import User
from app.models.project import Project
from app.dependencies import get_current_user
from typing import List
from uuid import UUID

router = APIRouter()

@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    data: ProjectRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    existing_user = (
        db.query(Project).filter(
            Project.owner_id == current_user.id,
            Project.name == data.name
        ).first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="project already exists"
        )
    
    project = Project(
        name=data.name,
        description=data.description,
        owner_id=current_user.id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project

@router.get("/projects", response_model=List[ProjectResponse], status_code=status.HTTP_200_OK)
def get_projects(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    
    projects = (
        db.query(Project).filter(
            Project.owner_id == current_user.id
        ).all()
    )

    return projects

@router.get("/projects/{id}", response_model=ProjectResponse, status_code=status.HTTP_200_OK)
def get_projects_by_id(
    id: UUID, # project id
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = (
        db.query(Project).filter(
            Project.id == id,
            Project.owner_id == current_user.id
        ).first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Project not found"
        )

    return project

@router.put("/projects/{id}", response_model=ProjectResponse, status_code=status.HTTP_200_OK)
def update_projects(
    id: UUID,
    data: ProjectUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    project = (
        db.query(Project).filter(
            Project.id == id,
            Project.owner_id == current_user.id
        ).first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if data.name is not None:
        duplicate = (
            db.query(Project).filter(
                Project.owner_id == current_user.id,
                Project.name == data.name,
                Project.id != id
            ).first()
        )

        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Project name already exists"
            )
    
        project.name = data.name

    if data.description is not None:
        project.description = data.description

    db.commit()
    db.refresh(project)

    return project
    

@router.delete("/projects/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    id: UUID, #project id
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = (
        db.query(Project).filter(
            Project.id == id,
            Project.owner_id == current_user.id
        ).first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully"
    }