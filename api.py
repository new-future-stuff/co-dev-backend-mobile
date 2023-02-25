from fastapi import APIRouter, HTTPException, status
from typing import List

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from models import Language, Project, Skill, TranslatedCountryName, engine, Country
from sqlmodel import select

router = APIRouter()


@router.post("/projects")
async def add_project(project: Project) -> Project:
    async with AsyncSession(engine) as session:
        session.add(project)
        await session.commit()
        await session.refresh(project)
    return project


@router.get("/projects")
async def get_projects() -> List[Project]:
    async with AsyncSession(engine) as session:
        results = (await session.execute(select(Project))).scalars().all()
        return results


@router.get("/projects/<project_id>")
async def get_project(project_id: int) -> Project:
    async with AsyncSession(engine) as session:
        result = (await session.execute(
            select(Project).filter(Project.id == project_id)
        )).scalars().one_or_none()
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return result


@router.get("/countries")
async def get_countries(language_id: int) -> List[TranslatedCountryName]:
    async with AsyncSession(engine) as session:
        results = (await session.execute(
            select(TranslatedCountryName)
            .filter(TranslatedCountryName.language_id == language_id)
        )).scalars().all()
        if not results:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return results


@router.get("/languages")
async def get_languages() -> List[Language]:
    async with AsyncSession(engine) as session:
        results = (await session.execute(select(Language))).scalars().all()
        return results


@router.get("/skills")
async def get_skills() -> List[Skill]:
    async with AsyncSession(engine) as session:
        results = (await session.execute(select(Skill))).scalars().all()
        return results
