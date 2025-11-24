from fastapi import FastAPI
from database import init_db
from routes import users, questions, quiz

app = FastAPI()

init_db()

app.include_router(users.router)
app.include_router(questions.router)
app.include_router(quiz.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)



#   "email": "admin@example.com",
#   "password": "admin123"
# }'
# {"accessToken":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsImV4cCI6MTc2MzgyNTIwMH0.C1ieotXu38MKrN6N3HF0yBg1-M2noW-6t1hAqkf4jfo"}