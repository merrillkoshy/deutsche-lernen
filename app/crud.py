from hashlib import sha256

from sqlalchemy.orm import Session

from app.models import Option, Question, Section, UserTable
from app.schema import User, UserCreate


def get_user(db: Session, user_id: str):
    return db.query(UserTable).filter(UserTable.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(UserTable).filter(UserTable.email == email).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = sha256(user.password.encode()).hexdigest()
    db_user = UserTable(email=user.email, hashed_password=hashed_password, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_sections_by_level(db: Session, level: str):
    return db.query(Section).filter(Section.level == level).all()


def get_questions_from_db(db: Session):
    return db.query(Question).join(Option).filter(Question.id == Option.question_id).all()
