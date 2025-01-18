from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False)
    topics = relationship("Topic", back_populates="user")

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    tags = Column(JSON, nullable=False)
    max_grade = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="topics")
    flashcards = relationship("Flashcard", back_populates="topic")
    crosswords = relationship("Crossword", back_populates="topic")

class Flashcard(Base):
    __tablename__ = "flashcards"
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, index=True, nullable=False)
    translation = Column(String, nullable=False)
    definition = Column(Text, nullable=True)
    examples = Column(JSON, nullable=True)
    img_path = Column(Text, nullable=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))

    topic = relationship("Topic", back_populates="flashcards")

class Crossword(Base):
    __tablename__ = "crosswords"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    grid = Column(JSON, nullable=False)
    clues = Column(JSON, nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"))

    topic = relationship("Topic", back_populates="crosswords")

class UserTopicGrade(Base):
    __tablename__ = "user_topic_grades"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    grade = Column(Integer, nullable=False)
    at = Column(DateTime, nullable=False)

