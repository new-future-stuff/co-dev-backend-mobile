import datetime
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
import secrets
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from models import ID, Language, Project, Skill, Token, TranslatedCountryName, User, engine
from sqlmodel import select

import security

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
async def get_project(project_id: ID) -> Project:
    async with AsyncSession(engine) as session:
        result = (await session.execute(
            select(Project).filter(Project.id == project_id)
        )).scalars().one_or_none()
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return result


@router.get("/countries")
async def get_countries(language_id: ID) -> List[TranslatedCountryName]:
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


class UserRegistrationData(BaseModel):
    name: str
    password: str
    email: str
    profile_picture_url: Optional[str]


class SafeUserData(BaseModel):
    id: ID
    name: str
    profile_picture_url: Optional[str]
    email: str

    @classmethod
    def make_from_user(cls, user: User) -> "SafeUserData":
        if user.id is None:
            raise Exception("This function does NOT accept unsaved users")
        return SafeUserData(
            id=user.id,
            name=user.name,
            profile_picture_url=user.profile_picture_url,
            email=user.email,
        )


@router.post("/users")
async def create_user(user_registration_data: UserRegistrationData) -> SafeUserData:
    salt = security.get_salt()
    user = User(
        name=user_registration_data.name,
        hashed_password=security.encrypt_password(
            password=user_registration_data.password,
            salt=salt,
        ),
        salt=salt,
        profile_picture_url=user_registration_data.profile_picture_url,
        email=user_registration_data.email,
    )
    async with AsyncSession(engine) as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return SafeUserData.make_from_user(user)


@router.get("/users")
async def get_users() -> List[SafeUserData]:
    async with AsyncSession(engine) as session:
        users: List[User] = (await session.execute(select(User))).scalars().all()
        return [SafeUserData.make_from_user(user) for user in users]


@router.get("/users/<user_id>")
async def get_user(user_id: int) -> SafeUserData:
    async with AsyncSession(engine) as session:
        try:
            user = (await session.execute(select(User).filter(User.id == user_id))).scalars().one()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return SafeUserData.make_from_user(user)


class UserAuthenticationData(BaseModel):
    email: int
    password: str


TOKEN_EXPIRATION_TIME = datetime.timedelta(days=7)


@router.post("/authenticate")
async def authenticate(authentication_data: UserAuthenticationData):
    async with AsyncSession(engine) as session:
        user: User = (await session.execute(select(User).filter(User.email == authentication_data.email))).scalars().one()
        if security.check_password(
            password=authentication_data.password,
            salt=user.salt,
            hashed_password=user.hashed_password,
        ):
            if user.id is None:
                raise Exception("A user without an ID - wtf? This should never happen")
            token = Token(
                owner_id=user.id,
                contents=secrets.token_urlsafe(32),
                expiration_date=datetime.datetime.now() + TOKEN_EXPIRATION_TIME,
            )
            session.add(token)
            await session.commit()
            await session.refresh(token)
            response = JSONResponse({"access_token": token.contents})
            response.set_cookie("ACCESS_TOKEN", token.contents)
