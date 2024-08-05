from typing import List

from fastapi import Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.crud import get_questions_from_db, get_sections_by_level
from app.main import fastapp, get_db
from app.schema import AnswerOption, Questions, Sections

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


@fastapp.get("/sections/{level}", response_model=List[Sections])
async def get_sections(level: str, db: Session = Depends(get_db)) -> List[Sections]:
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
def get_questions(db: Session = Depends(get_db)) -> List[Questions]:
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
            )
        )
    return data
