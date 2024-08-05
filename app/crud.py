from sqlalchemy.orm import Session

from app.models import Option, Question, Section


def get_sections_by_level(db: Session, level: str):
    return db.query(Section).filter(Section.level == level).all()


def get_questions_from_db(db: Session):
    return db.query(Question).join(Option).filter(Question.id == Option.question_id).all()
