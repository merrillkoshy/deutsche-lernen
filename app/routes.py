import json
from datetime import timedelta
from typing import Annotated, List

from fastapi import Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.authentication import get_current_user
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.crud import get_questions_from_db, get_sections_by_level, get_user, get_user_by_email
from app.main import fastapp, get_db
from app.schema import AnswerOption, LoginRequest, Questions, Sections, Token, User, UserCreate
from app.services import create_access_token, verify_password

origins = {
    "https://merrillkoshy.github.io/",
    "http://localhost",
    "http://localhost:5173",
}

fastapp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@fastapp.get("/")
def read_root():
    return {"Hello": "World"}


@fastapp.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    email = request.email
    password = request.password
    db_user = get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    data = {"access_token": access_token, "token_type": "bearer", "user_id": str(db_user.id)}
    return data


@fastapp.get("/sections/{level}", response_model=List[Sections])
async def get_sections(
    level: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> List[Sections]:
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    sections = get_sections_by_level(db, level=level)
    data = []
    if sections is None:
        raise HTTPException(status_code=410, detail="Gone baby gone")

    for section in sections:
        questions: list[Questions] = []
        for question in section.questions:
            questions.append(question)
        data.append(
            Sections(
                id=section.id,
                section=section.section,
                level=section.level,
                questions=questions,
            )
        )
    return data


@fastapp.get("/questions", response_model=List[Questions])
def get_questions(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> List[Questions]:
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    questions = get_questions_from_db(db)

    data = []
    if questions is None:
        raise HTTPException(status_code=410, detail="Gone baby gone")

    for question in questions:
        options: list[AnswerOption] = []
        for option in question.options:
            options.append({"id": option.id, "option": option.option})
        data.append(
            Questions(
                id=question.id,
                question=question.question,
                answer=question.answer,
                options=options,
                question_type=question.question_type,
            )
        )
    return data


@fastapp.post("/users", response_model=User)
def create_user(
    user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@fastapp.get("/users/{user_id}", response_model=User)
def read_user(
    user_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    data = User(
        id=str(db_user.id),
        email=db_user.email,
        full_name=db_user.full_name,
        access=db_user.access,
    )
    return data
