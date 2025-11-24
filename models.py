from sqlmodel import SQLModel, Field
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    hashed_password: str
    is_admin: bool = False

class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    options: str
    correct_answer: str

class QuizAttempt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    score: int
    total_questions: int
    attempted_at: datetime = Field(default_factory=datetime.utcnow)

class AttemptAnswer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    attempt_id: int
    question_id: int
    selected_option: str
    is_correct: bool
    attempted_at: datetime = Field(default_factory=datetime.utcnow)
class Result(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    score: int

class UserRegister(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class QuestionCreate(BaseModel):
    text: str
    options: List[str]
    correct_answer: str

class QuizSubmission(BaseModel):
    answers: dict