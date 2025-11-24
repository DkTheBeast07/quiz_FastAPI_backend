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

**POST /login** - Login user (form data)
```bash
curl -X POST "http://localhost:8000/login" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=admin@example.com&password=securepassword"
```
Response: `{"access_token": "<JWT_TOKEN>", "token_type": "bearer"}`

### Protected Routes (Admin Only)
**POST /questions** - Create question
**GET /questions** - Get all questions
**GET /questions/{id}** - Get question by ID
**PUT /questions/{id}** - Update question
**DELETE /questions/{id}** - Delete question

### Quiz Routes (All Users)
**GET /quiz** - Get 2 random questions
**POST /quiz/result** - Submit answers and get score

### Quiz Attempt Tracking (NEW)
**GET /quiz/attempts** - Get user's quiz attempt history
**GET /quiz/attempts/{id}** - Get detailed attempt breakdown
**GET /quiz/attempts/all** - Get all attempts (Admin only)

*All protected routes require: `Authorization: Bearer <token>`*

## ✨ Features

- **JWT Authentication** with role-based access control
- **Admin CRUD Operations** for question management
- **Quiz System** with random question selection
- **Attempt Tracking** with detailed analytics
- **Security** with proper authorization checks
- **Swagger UI** for interactive API testing

## 🧪 Quick Test

1. **Create Admin:** Register with `admin@example.com`
2. **Create User:** Register with any other email
3. **Login:** Get JWT tokens for both (use form data)
4. **Admin:** Manage questions with admin token
5. **User:** Take quiz and view attempt history
6. **Analytics:** Admin can view all user attempts

## 📚 Documentation

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## 🔒 Security

- Password hashing with bcrypt
- JWT token authentication
- Role-based access control
- Protected admin endpoints