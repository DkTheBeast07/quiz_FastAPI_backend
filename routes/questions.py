import json
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Question, QuestionCreate
from auth import get_current_user

router = APIRouter()

@router.post("/questions")
def create_question(question_data: QuestionCreate, session: Session = Depends(get_session), user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    q = Question(
        text=question_data.text, 
        options=json.dumps(question_data.options), 
        correct_answer=question_data.correct_answer
    )

    session.add(q)
    session.commit()
    session.refresh(q)
    return {"id": q.id, "text": q.text, "options": json.loads(q.options), "correct_answer": q.correct_answer}

@router.get("/questions")
def list_questions(session: Session = Depends(get_session), user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    questions = session.exec(select(Question)).all()
    return [{"id": q.id, "text": q.text, "options": json.loads(q.options), "correct_answer": q.correct_answer} for q in questions]


@router.get("/questions/{id}")
def get_question(id: int, session: Session = Depends(get_session), user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    q = session.get(Question, id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"id": q.id, "text": q.text, "options": json.loads(q.options), "correct_answer": q.correct_answer}

@router.put("/questions/{id}")
def update_question(id: int, question_data: QuestionCreate, session: Session = Depends(get_session), user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    q = session.get(Question, id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    q.text = question_data.text
    q.options = json.dumps(question_data.options)
    q.correct_answer = question_data.correct_answer
    session.add(q)
    session.commit()
    print(q.options)
    print("ghjk")
    session.refresh(q)
    return {"id": q.id, "text": q.text, "options": json.loads(q.options), "correct_answer": q.correct_answer}

@router.delete("/questions/{id}")
def delete_question(id: int, session: Session = Depends(get_session), user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    q = session.get(Question, id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    session.delete(q)
    session.commit()
    return {"message": f"Question {id} deleted successfully"}