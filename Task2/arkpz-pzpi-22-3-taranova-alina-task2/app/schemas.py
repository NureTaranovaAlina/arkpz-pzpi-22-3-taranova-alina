from pydantic import BaseModel
from typing import Optional, List, Dict


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class FlashcardBase(BaseModel):
    word: str
    translation: str
    definition: Optional[str] = None
    examples: Optional[List[str]] = None
    tags: Optional[List[str]] = None


class FlashcardCreate(FlashcardBase):
    pass


class Flashcard(FlashcardBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class CrosswordBase(BaseModel):
    title: str
    grid: List[List[str]]
    clues: Dict[str, Dict[str, str]]


class CrosswordCreate(CrosswordBase):
    pass


class Crossword(CrosswordBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
