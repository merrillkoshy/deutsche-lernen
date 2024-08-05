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
