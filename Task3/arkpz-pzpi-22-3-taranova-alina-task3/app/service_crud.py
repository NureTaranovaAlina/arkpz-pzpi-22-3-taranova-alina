from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password, is_admin=user.is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_topic(db: Session, topic: schemas.TopicCreate, user_id: int):
    db_topic = models.Topic(topic.dict(), user_id = user_id)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

def get_topics_by_user_id(db: Session, user_id: int):
    return db.query(models.Topic).filter(models.Topic.user_id == user_id).all()

def create_flashcard(db: Session, flashcard: schemas.FlashcardCreate):
    db_flashcard = models.Flashcard(**flashcard.dict())
    db.add(db_flashcard)
    db.commit()
    db.refresh(db_flashcard)
    return db_flashcard

def get_flashcards_by_topic_id(db: Session, topic_id: int):
    return db.query(models.Flashcard).filter(models.Flashcard.topic_id == topic_id).all()

def update_flashcard_image(db: Session, flashcard_id: int, image_path: str):
    flashcard = db.query(models.Flashcard).filter(models.Flashcard.id == flashcard_id).first()
    if flashcard:
        flashcard.image_path = image_path # type: ignore
        db.commit()
        db.refresh(flashcard)
    return flashcard

def get_flashcard_by_id(db: Session, flashcard_id: int):
    return db.query(models.Flashcard).filter(models.Flashcard.id == flashcard_id).first()

def create_crossword(db: Session, crossword: schemas.CrosswordCreate):
    db_crossword = models.Crossword(**crossword.dict())
    db.add(db_crossword)
    db.commit()
    db.refresh(db_crossword)
    return db_crossword

def get_crosswords_by_topic_id(db: Session, topic_id: int):
    return db.query(models.Crossword).filter(models.Crossword.topic_id == topic_id).all()

def put_user_topic_grade(db: Session, user_topic_grade: schemas.UserTopicGradeCreate, user_id: int):
    db_grading = models.UserTopicGrade(user_topic_grade.dict(), user_id=user_id)
    db.add(db_grading)
    db.commit()
    db.refresh(db_grading)
    return db_grading

def get_all_user_grades(db: Session, user_id: int) :
    return db.query(models.UserTopicGrade).filter(models.UserTopicGrade.user_id == user_id).all()

from datetime import timedelta
from app.models import User, UserTopicGrade

def get_repetition_schedule(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError(f"User with ID {user_id} not found")

    schedule = {}
    one_week = timedelta(days=7)
    today = datetime.now().date()

    for topic in user.topics:
        last_grade = (
            db.query(UserTopicGrade)
            .filter(UserTopicGrade.user_id == user_id, UserTopicGrade.topic_id == topic.id)
            .order_by(UserTopicGrade.at.desc())  
            .first()
        )

        if last_grade:
            next_review_date = (last_grade.at + one_week).date()
        else:
            next_review_date = today

        if next_review_date >= today:
            schedule[topic.id] = next_review_date.strftime("%Y-%m-%d")

    return schedule
