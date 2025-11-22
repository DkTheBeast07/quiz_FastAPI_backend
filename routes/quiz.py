import random
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Question, Result, QuizSubmission
from auth import get_current_user

router = APIRouter()

@router.get("/quiz")
def get_quiz(session: Session = Depends(get_session), user=Depends(get_current_user)):
    questions = session.exec(select(Question)).all()
    if len(questions) < 2:
        raise HTTPException(status_code=400, detail="Not enough questions available")
    sample = random.sample(questions, min(2, len(questions)))
    return [{"id": q.id, "text": q.text, "options": json.loads(q.options)} for q in sample]

@router.post("/quiz/result")
def submit_quiz(submission: QuizSubmission, session: Session = Depends(get_session), user=Depends(get_current_user)):
    score = 0
    correct_answers = {}
    for qid, ans in submission.answers.items():
        q = session.get(Question, int(qid))
        if q:
            correct_answers[qid] = q.correct_answer
            if ans == q.correct_answer:
                score += 1
    result = Result(user_id=user.id, score=score)
    session.add(result)
    session.commit()
    return {"score": score, "correct_answers": correct_answers}