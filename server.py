from typing import List, Optional
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlmodel import Relationship, SQLModel, create_engine, Session, select, Field
from sqlalchemy.exc import IntegrityError


class ProjectSkillLink(SQLModel, table=True):
    project_id: int = Field(foreign_key="project.id", primary_key=True)
    skill_id: int = Field(foreign_key="skill.id", primary_key=True)


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    creator_id: int
    reward: str
    required_skills: List["Skill"] = Relationship(back_populates="related_projects", link_model=ProjectSkillLink)


class Skill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    related_projects: List[Project] = Relationship(back_populates="required_skills", link_model=ProjectSkillLink)


app = FastAPI()
engine = create_engine("sqlite:///db.sqlite3", echo=True, connect_args={"check_same_thread": False})


@app.exception_handler(IntegrityError)
async def add_process_time_header(request: Request, exc: IntegrityError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"integrity_error": exc.orig.args[0]})


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.post("/api/projects")
async def add_project(project: Project) -> Project:
    with Session(engine) as session:
        session.add(project)
        session.commit()
        session.refresh(project)
    return project


@app.get("/api/projects")
async def get_projects() -> List[Project]:
    with Session(engine) as session:
        results = session.exec(select(Project)).all()
        return results


@app.get("/api/projects/<project_id>")
async def get_project(project_id: int) -> Project:
    with Session(engine) as session:
        result = session.exec(select(Project).filter(Project.id == project_id)).one_or_none()
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return result
