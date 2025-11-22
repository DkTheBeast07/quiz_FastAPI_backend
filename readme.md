# Quiz FastAPI Backend

A secure backend API for quiz management, built with FastAPI, SQLModel, and JWT authentication.

## 🔧 Tech Stack
- FastAPI
- SQLModel (SQLite)
- JWT (python-jose)
- Passlib (bcrypt)
- Uvicorn

## 🚀 Setup

```bash
pip install -r requirements.txt
python main.py
```

## 👥 User Types

### Admin User
- **Email:** `admin@example.com` (automatically gets admin privileges)
- **Can:** Create, read, update, delete questions
- **Access:** All endpoints

### Regular User  
- **Email:** Any other email
- **Can:** Take quizzes only
- **Access:** Quiz endpoints only

## 📋 API Endpoints

### Authentication
**POST /register** - Register user
```json
{
  "email": "admin@example.com",
  "password": "securepassword"
}
```

**POST /login** - Login user
```json
{
  "email": "admin@example.com",
  "password": "securepassword"
}
```
Response: `{"accessToken": "<JWT_TOKEN>"}`

### Protected Routes (Admin Only)
**POST /questions** - Create question
**GET /questions** - Get all questions
**GET /questions/{id}** - Get question by ID
**PUT /questions/{id}** - Update question
**DELETE /questions/{id}** - Delete question

### Quiz Routes (All Users)
**GET /quiz** - Get 2 random questions
**POST /quiz/result** - Submit answers and get score

*All protected routes require: `Authorization: Bearer <token>`*

## 🧪 Quick Test

1. **Create Admin:** Register with `admin@example.com`
2. **Create User:** Register with any other email
3. **Login:** Get JWT tokens for both
4. **Admin:** Manage questions with admin token
5. **User:** Take quiz with user token