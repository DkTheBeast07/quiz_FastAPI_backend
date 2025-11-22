from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Question
from ..auth import get_current_user

router = APIRouter()

#  Create Question (Admin only)
@router.post("/questions")
def create_question(text: str, options: str, correct_answer: str,
                    session: Session = Depends(get_session),
                    user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    q = Question(text=text, options=options, correct_answer=correct_answer)
    session.add(q)
    session.commit()
    session.refresh(q)
    return q

#  Get All Questions (Admin only)
@router.get("/questions")
def list_questions(session: Session = Depends(get_session), user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    return session.exec(select(Question)).all()

#  Get Question by ID (Admin only)
@router.get("/questions/{id}")
def get_question(id: int, session: Session = Depends(get_session), user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    q = session.get(Question, id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q

#  Update Question by ID (Admin only)
@router.put("/questions/{id}")
def update_question(id: int, text: str, options: str, correct_answer: str,
                    session: Session = Depends(get_session),
                    user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    q = session.get(Question, id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    q.text = text
    q.options = options
    q.correct_answer = correct_answer
    session.add(q)
    session.commit()
    session.refresh(q)
    return q

#  Delete Question by ID (Admin only)
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