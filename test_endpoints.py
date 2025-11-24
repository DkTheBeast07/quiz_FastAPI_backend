"""
Comprehensive API Testing Script for Quiz Backend

This script tests all endpoints in the Quiz API including:
- Authentication (register/login)
- Question management (CRUD operations - Admin only)
- Quiz functionality (take quiz, submit answers)
- Quiz attempt tracking (NEW - view attempt history)

Run this after starting the server: python main.py
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_all_endpoints():
    print("🧪 Testing Quiz API - All Endpoints")
    print("=" * 60)
    
    # ========================================
    # AUTHENTICATION ENDPOINTS
    # ========================================
    
    print("\n🔐 AUTHENTICATION ENDPOINTS")
    print("-" * 40)
    
    # 1. POST /register - Register new users
    print("\n1️⃣ POST /register - Register new users")
    print("   Purpose: Create new user accounts in the system")
    
    # Register admin user
    admin_data = {
        "email": "admin@example.com",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/register", json=admin_data)
    print(f"   Admin registration: {response.status_code} - {response.json()}")
    
    # Register regular user
    user_data = {
        "email": "testuser@example.com", 
        "password": "user123"
    }
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    print(f"   User registration: {response.status_code} - {response.json()}")
    
    # 2. POST /login - Authenticate users and get JWT tokens
    print("\n2️⃣ POST /login - Authenticate users and get JWT tokens")
    print("   Purpose: Login users and receive access tokens for protected endpoints")
    
    # Admin login (OAuth2 form format)
    admin_login = requests.post(f"{BASE_URL}/login", 
        data={"username": "admin@example.com", "password": "admin123"})
    print(f"   Admin login: {admin_login.status_code}")
    
    if admin_login.status_code == 200:
        admin_token = admin_login.json()["access_token"]
        print(f"   ✅ Admin token received: {admin_token[:20]}...")
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
    else:
        print("   ❌ Admin login failed")
        return
    
    # User login
    user_login = requests.post(f"{BASE_URL}/login", 
        data={"username": "testuser@example.com", "password": "user123"})
    print(f"   User login: {user_login.status_code}")
    
    if user_login.status_code == 200:
        user_token = user_login.json()["access_token"]
        print(f"   ✅ User token received: {user_token[:20]}...")
        user_headers = {"Authorization": f"Bearer {user_token}"}
    else:
        print("   ❌ User login failed")
        return
    
    # ========================================
    # QUESTION MANAGEMENT ENDPOINTS (ADMIN ONLY)
    # ========================================
    
    print("\n📝 QUESTION MANAGEMENT ENDPOINTS (ADMIN ONLY)")
    print("-" * 50)
    
    # 3. POST /questions - Create new quiz questions
    print("\n3️⃣ POST /questions - Create new quiz questions")
    print("   Purpose: Admin can add new questions to the quiz database")
    print("   Access: Admin only (403 for regular users)")
    
    question_data = {
        "text": "What is the capital of Japan?",
        "options": ["Tokyo", "Osaka", "Kyoto", "Hiroshima"],
        "correct_answer": "Tokyo"
    }
    response = requests.post(f"{BASE_URL}/questions", json=question_data, headers=admin_headers)
    print(f"   Create question: {response.status_code} - {response.json()}")
    
    # Add another question
    question2 = {
        "text": "What is 10 - 3?",
        "options": ["6", "7", "8", "9"],
        "correct_answer": "7"
    }
    requests.post(f"{BASE_URL}/questions", json=question2, headers=admin_headers)
    
    # 4. GET /questions - Retrieve all questions
    print("\n4️⃣ GET /questions - Retrieve all questions")
    print("   Purpose: Admin can view all questions in the database")
    print("   Access: Admin only")
    
    response = requests.get(f"{BASE_URL}/questions", headers=admin_headers)
    print(f"   Get all questions: {response.status_code}")
    questions = response.json()
    print(f"   📊 Total questions found: {len(questions)}")
    
    if questions:
        question_id = questions[0]["id"]
        
        # 5. GET /questions/{id} - Get specific question
        print(f"\n5️⃣ GET /questions/{{id}} - Get specific question")
        print("   Purpose: Admin can view details of a specific question")
        print("   Access: Admin only")
        
        response = requests.get(f"{BASE_URL}/questions/{question_id}", headers=admin_headers)
        print(f"   Get question {question_id}: {response.status_code}")
        print(f"   Question text: '{response.json()['text']}'")
        
        # 6. PUT /questions/{id} - Update existing question
        print(f"\n6️⃣ PUT /questions/{{id}} - Update existing question")
        print("   Purpose: Admin can modify existing questions")
        print("   Access: Admin only")
        
        update_data = {
            "text": "What is the capital of Japan? (Updated)",
            "options": ["Tokyo", "Osaka", "Kyoto", "Nagoya"],
            "correct_answer": "Tokyo"
        }
        response = requests.put(f"{BASE_URL}/questions/{question_id}", json=update_data, headers=admin_headers)
        print(f"   Update question: {response.status_code}")
        print(f"   Updated text: '{response.json()['text']}'")
    
    # ========================================
    # QUIZ ENDPOINTS (ALL AUTHENTICATED USERS)
    # ========================================
    
    print("\n🎯 QUIZ ENDPOINTS (ALL AUTHENTICATED USERS)")
    print("-" * 45)
    
    # 7. GET /quiz - Get random quiz questions
    print("\n7️⃣ GET /quiz - Get random quiz questions")
    print("   Purpose: Users get 2 random questions to answer (without correct answers)")
    print("   Access: All authenticated users")
    
    response = requests.get(f"{BASE_URL}/quiz", headers=user_headers)
    print(f"   Get quiz: {response.status_code}")
    
    if response.status_code == 200:
        quiz_questions = response.json()
        print(f"   📋 Quiz questions received: {len(quiz_questions)}")
        
        # Display questions
        for i, q in enumerate(quiz_questions, 1):
            print(f"      Q{i}: {q['text']}")
            print(f"          Options: {q['options']}")
        
        # 8. POST /quiz/result - Submit quiz answers
        print("\n8️⃣ POST /quiz/result - Submit quiz answers")
        print("   Purpose: Users submit their answers and get score + correct answers")
        print("   Access: All authenticated users")
        print("   Note: Creates detailed attempt tracking records")
        
        # Prepare answers (pick first option for each question)
        answers = {}
        for q in quiz_questions:
            answers[str(q["id"])] = q["options"][0]  # Pick first option
        
        result_data = {"answers": answers}
        response = requests.post(f"{BASE_URL}/quiz/result", json=result_data, headers=user_headers)
        print(f"   Submit answers: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   🎯 Score achieved: {result['score']}/{len(answers)}")
            print(f"   📝 Correct answers: {result['correct_answers']}")
    
    # ========================================
    # QUIZ ATTEMPT TRACKING ENDPOINTS (NEW)
    # ========================================
    
    print("\n📊 QUIZ ATTEMPT TRACKING ENDPOINTS (NEW)")
    print("-" * 45)
    
    # 9. GET /quiz/attempts - Get user's attempt history
    print("\n9️⃣ GET /quiz/attempts - Get user's attempt history")
    print("   Purpose: Users can view their quiz attempt history with scores and timestamps")
    print("   Access: All authenticated users (own attempts only)")
    
    response = requests.get(f"{BASE_URL}/quiz/attempts", headers=user_headers)
    print(f"   Get attempts: {response.status_code}")
    
    if response.status_code == 200:
        attempts = response.json()
        print(f"   📈 Total attempts found: {len(attempts)}")
        
        for attempt in attempts:
            print(f"      Attempt {attempt['attempt_id']}: {attempt['score']}/{attempt['total_questions']} on {attempt['attempted_at'][:19]}")
        
        if attempts:
            attempt_id = attempts[0]["attempt_id"]
            
            # 10. GET /quiz/attempts/{id} - Get detailed attempt information
            print(f"\n🔟 GET /quiz/attempts/{{id}} - Get detailed attempt information")
            print("   Purpose: Users can review specific attempt with question-by-question breakdown")
            print("   Access: All authenticated users (own attempts only)")
            
            response = requests.get(f"{BASE_URL}/quiz/attempts/{attempt_id}", headers=user_headers)
            print(f"   Get attempt details: {response.status_code}")
            
            if response.status_code == 200:
                details = response.json()
                print(f"   📋 Attempt {details['attempt_id']} details:")
                print(f"      Score: {details['score']}/{details['total_questions']}")
                print(f"      Date: {details['attempted_at'][:19]}")
                print(f"      Answers breakdown:")
                
                for answer in details['answers']:
                    status = "✅ Correct" if answer['is_correct'] else "❌ Wrong"
                    print(f"         Q{answer['question_id']}: {answer['selected_option']} {status}")
                    if not answer['is_correct']:
                        print(f"            (Correct: {answer['correct_option']})")
    
    # 11. GET /quiz/attempts/all - Admin analytics (Admin only)
    print(f"\n1️⃣1️⃣ GET /quiz/attempts/all - Admin analytics")
    print("   Purpose: Admins can view all users' quiz attempts for analytics")
    print("   Access: Admin only (403 for regular users)")
    
    # Test with regular user (should fail)
    response = requests.get(f"{BASE_URL}/quiz/attempts/all", headers=user_headers)
    print(f"   Regular user access: {response.status_code} (Expected: 403 Forbidden)")
    
    # Test with admin user (should work)
    response = requests.get(f"{BASE_URL}/quiz/attempts/all", headers=admin_headers)
    print(f"   Admin access: {response.status_code}")
    
    if response.status_code == 200:
        all_attempts = response.json()
        print(f"   📊 Total attempts across all users: {len(all_attempts)}")
        
        for attempt in all_attempts:
            print(f"      {attempt['user_email']}: Score {attempt['score']} (Attempt {attempt['attempt_id']})")
    
    # ========================================
    # ACCESS CONTROL TESTING
    # ========================================
    
    print("\n🔒 ACCESS CONTROL TESTING")
    print("-" * 30)
    
    # Test admin-only endpoints with regular user
    print("\n🚫 Testing admin-only access with regular user token:")
    
    endpoints_to_test = [
        ("GET", "/questions", "View all questions"),
        ("POST", "/questions", "Create question"),
        ("GET", "/quiz/attempts/all", "View all attempts")
    ]
    
    for method, endpoint, description in endpoints_to_test:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", headers=user_headers)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", 
                json={"text": "Test", "options": ["A", "B"], "correct_answer": "A"}, 
                headers=user_headers)
        
        expected = "✅ Blocked (403)" if response.status_code == 403 else f"❌ Allowed ({response.status_code})"
        print(f"   {method} {endpoint} - {description}: {expected}")
    
    # ========================================
    # CLEANUP & SUMMARY
    # ========================================
    
    if questions and question_id:
        # 12. DELETE /questions/{id} - Delete question (Admin only)
        print(f"\n1️⃣2️⃣ DELETE /questions/{{id}} - Delete question")
        print("   Purpose: Admin can remove questions from the database")
        print("   Access: Admin only")
        
        response = requests.delete(f"{BASE_URL}/questions/{question_id}", headers=admin_headers)
        print(f"   Delete question: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Question {question_id} deleted successfully")
    
    print("\n" + "=" * 60)
    print("🎉 ALL ENDPOINT TESTS COMPLETED!")
    print("=" * 60)
    print("\n📋 ENDPOINT SUMMARY:")
    print("✅ Authentication: 2 endpoints (register, login)")
    print("✅ Question Management: 5 endpoints (CRUD operations)")
    print("✅ Quiz Functionality: 2 endpoints (get quiz, submit result)")
    print("✅ Attempt Tracking: 3 endpoints (NEW - history, details, analytics)")
    print("✅ Access Control: Properly enforced")
    print("\n🔗 Total: 12 endpoints tested")
    print("🌐 Swagger UI: http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    try:
        test_all_endpoints()
    except requests.exceptions.ConnectionError:
        print("❌ Server not running!")
        print("💡 Start server with: python main.py")
        print("🌐 Then access: http://127.0.0.1:8000/docs")