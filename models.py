from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, Field


ID = int


class UserSkillLink(SQLModel, table=True):
    user_id: ID = Field(foreign_key="user.id", primary_key=True)
    skill_id: ID = Field(foreign_key="skill.id", primary_key=True)


class User(SQLModel, table=True):
    id: Optional[ID] = Field(default=None, primary_key=True)
    name: str
    hashed_password: bytes
    salt: bytes
    profile_picture_url: Optional[str]
    email: str = Field(unique=True, index=True)


class ProjectSkillLink(SQLModel, table=True):
    project_id: ID = Field(foreign_key="project.id", primary_key=True)
    skill_id: ID = Field(foreign_key="skill.id", primary_key=True)


class Language(SQLModel, table=True):
    id: Optional[ID] = Field(default=None, primary_key=True)
    name: str


class Project(SQLModel, table=True):
    id: Optional[ID] = Field(default=None, primary_key=True)
    name: str
    description: str
    creator_id: ID = Field(foreign_key="user.id")
    reward: int
    currency: str
    logo_url: Optional[str]


class Skill(SQLModel, table=True):
    id: Optional[ID] = Field(default=None, primary_key=True)
    name: str


class Country(SQLModel, table=True):
    id: Optional[ID] = Field(default=None, primary_key=True)


class TranslatedCountryName(SQLModel, table=True):
    country_id: ID = Field(foreign_key="country.id", primary_key=True)
    name: str
    language_id: ID = Field(foreign_key="language.id", primary_key=True)


engine = create_async_engine("sqlite+aiosqlite:///db.sqlite3", echo=True, connect_args={"check_same_thread": False})
