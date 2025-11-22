import random
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..database import get_session
from ..models import Question, Result
from ..auth import get_current_user

router = APIRouter()

@router.get("/quiz")
def get_quiz(session: Session = Depends(get_session), user=Depends(get_current_user)):
    questions = session.exec(select(Question)).all()
    sample = random.sample(questions, 2)
    return [{"id": q.id, "text": q.text, "options": q.options} for q in sample]

@router.post("/quiz/result")
def submit_quiz(answers: dict, session: Session = Depends(get_session), user=Depends(get_current_user)):
    score = 0
    correct_answers = {}
    for qid, ans in answers.items():
        q = session.get(Question, qid)
        if q:
            correct_answers[qid] = q.correct_answer
            if ans == q.correct_answer:
                score += 1
    result = Result(user_id=user.id, score=score)
    session.add(result)
    session.commit()
    return {"score": score, "correct_answers": correct_answers}