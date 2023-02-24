from fastapi import APIRouter, HTTPException, status
from typing import List
from models import Project, engine, Country
from sqlmodel import Session, select

router = APIRouter()


@router.post("/projects")
async def add_project(project: Project) -> Project:
    with Session(engine) as session:
        session.add(project)
        session.commit()
        session.refresh(project)
    return project


@router.get("/projects")
async def get_projects() -> List[Project]:
    with Session(engine) as session:
        results = session.exec(select(Project)).all()
        return results


@router.get("/projects/<project_id>")
async def get_project(project_id: int) -> Project:
    with Session(engine) as session:
        result = session.exec(select(Project).filter(Project.id == project_id)).one_or_none()
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return result


@router.get("/countries")
async def get_countries() -> List[Country]:
    with Session(engine) as session:
        results = session.exec(select(Country)).all()
        return results
