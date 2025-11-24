import random
import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Question, Result, QuizSubmission, QuizAttempt, AttemptAnswer, User
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
    total_questions = len(submission.answers)
    correct_answers = {}
    
    # Create quiz attempt
    attempt = QuizAttempt(
        user_id=user.id,
        score=0,  # Will update after calculating
        total_questions=total_questions
    )
    session.add(attempt)
    session.commit()
    session.refresh(attempt)
    
    # Process each answer
    for qid, ans in submission.answers.items():
        q = session.get(Question, int(qid))
        if q:
            correct_answers[qid] = q.correct_answer
            is_correct = ans == q.correct_answer
            if is_correct:
                score += 1
            
            # Save attempt answer
            attempt_answer = AttemptAnswer(
                attempt_id=attempt.id,
                question_id=int(qid),
                selected_option=ans,
                is_correct=is_correct
            )
            session.add(attempt_answer)
    
    # Update attempt with final score
    attempt.score = score
    session.add(attempt)
    session.commit()
    
    # Keep old Result for backward compatibility
    result = Result(user_id=user.id, score=score)
    session.add(result)
    session.commit()
    
    return {"score": score, "correct_answers": correct_answers}

@router.get("/quiz/attempts")
def get_user_attempts(session: Session = Depends(get_session), user=Depends(get_current_user)):
    attempts = session.exec(select(QuizAttempt).where(QuizAttempt.user_id == user.id)).all()
    return [
        {
            "attempt_id": attempt.id,
            "score": attempt.score,
            "total_questions": attempt.total_questions,
            "attempted_at": attempt.attempted_at.isoformat()
        }
        for attempt in attempts
    ]

@router.get("/quiz/attempts/all")
def get_all_attempts(session: Session = Depends(get_session), user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    
    attempts = session.exec(select(QuizAttempt)).all()
    result = []
    
    for attempt in attempts:
        user_obj = session.get(User, attempt.user_id)
        if user_obj:
            result.append({
                "user_email": user_obj.email,
                "attempt_id": attempt.id,
                "score": attempt.score,
                "attempted_at": attempt.attempted_at.isoformat()
            })
    
    return result

@router.get("/quiz/attempts/{attempt_id}")
def get_attempt_details(attempt_id: int, session: Session = Depends(get_session), user=Depends(get_current_user)):
    attempt = session.get(QuizAttempt, attempt_id)
    if not attempt or attempt.user_id != user.id:
        raise HTTPException(status_code=404, detail="Attempt not found")
    
    answers = session.exec(select(AttemptAnswer).where(AttemptAnswer.attempt_id == attempt_id)).all()
    answer_details = []
    
    for answer in answers:
        question = session.get(Question, answer.question_id)
        if question:
            answer_details.append({
                "question_id": answer.question_id,
                "question_text": question.text,
                "selected_option": answer.selected_option,
                "is_correct": answer.is_correct,
                "correct_option": question.correct_answer
            })
    
    return {
        "attempt_id": attempt.id,
        "score": attempt.score,
        "total_questions": attempt.total_questions,
        "attempted_at": attempt.attempted_at.isoformat(),
        "answers": answer_details
    }