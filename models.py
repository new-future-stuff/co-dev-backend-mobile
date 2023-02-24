from typing import Optional, List
from sqlmodel import Relationship, SQLModel, Field, create_engine


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


class Country(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


engine = create_engine("sqlite:///db.sqlite3", echo=True, connect_args={"check_same_thread": False})
