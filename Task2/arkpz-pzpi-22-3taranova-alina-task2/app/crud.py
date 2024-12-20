from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_flashcard(db: Session, flashcard: schemas.FlashcardCreate, user_id: int):
    db_flashcard = models.Flashcard(**flashcard.dict(), owner_id=user_id)
    db.add(db_flashcard)
    db.commit()
    db.refresh(db_flashcard)
    return db_flashcard


def get_flashcards(db: Session, user_id: int):
    return db.query(models.Flashcard).filter(models.Flashcard.owner_id == user_id).all()


def create_crossword(db: Session, crossword: schemas.CrosswordCreate, user_id: int):
    db_crossword = models.Crossword(**crossword.dict(), owner_id=user_id)
    db.add(db_crossword)
    db.commit()
    db.refresh(db_crossword)
    return db_crossword


def get_crosswords(db: Session, user_id: int):
    return db.query(models.Crossword).filter(models.Crossword.owner_id == user_id).all()
