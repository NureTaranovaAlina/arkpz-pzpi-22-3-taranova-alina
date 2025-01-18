from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    is_admin: bool

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

# Topic schemas
class TopicBase(BaseModel):
    title: str
    description: Optional[str] = None
    tags: List[str]
    max_grade: int

class TopicCreate(TopicBase):
    pass

class TopicResponse(TopicBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# Flashcard schemas
class FlashcardBase(BaseModel):
    word: str
    translation: str
    definition: Optional[str] = None
    examples: Optional[List[str]] = None
    img_path: Optional[str] = None
    topic_id: int 

class FlashcardCreate(FlashcardBase):
    pass

class FlashcardResponse(FlashcardBase):
    id: int

    class Config:
        orm_mode = True

# Crossword schemas
class CrosswordBase(BaseModel):
    title: str
    grid: dict
    clues: dict
    topic_id: int

class CrosswordCreate(CrosswordBase):
    pass

class CrosswordResponse(CrosswordBase):
    id: int

    class Config:
        orm_mode = True

# UserTopicGrade schemas
class UserTopicGradeBase(BaseModel):
    grade: int
    topic_id: int
    at: datetime

class UserTopicGradeCreate(UserTopicGradeBase):
    pass

class UserTopicGradeResponse(UserTopicGradeBase):
    id: int
    user_id: int
 
    class Config:
        orm_mode = True

# Combined schemas for nested responses
class TopicWithRelationsResponse(TopicResponse):
    flashcards: List[FlashcardResponse] = []
    crosswords: List[CrosswordResponse] = []

class UserWithTopicsResponse(UserResponse):
    topics: List[TopicResponse] = []
