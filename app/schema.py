from typing import List
from uuid import UUID

from pydantic import BaseModel


class AnswerOption(BaseModel):
    id: UUID
    option: str

    class Config:
        orm_mode = True


class Questions(BaseModel):
    id: UUID
    question: str
    answer: str
    question_type: str
    options: List[AnswerOption]

    class Config:
        orm_mode = True


class Sections(BaseModel):
    id: UUID
    section: str
    level: str
    questions: List[Questions]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    full_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    email: str
    full_name: str
    access: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str


class LoginRequest(BaseModel):
    email: str
    password: str
