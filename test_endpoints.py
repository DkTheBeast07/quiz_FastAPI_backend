import requests
import json

BASE_URL = "http://localhost:8000"

def test_all_endpoints():
    print("🧪 Testing Quiz API Endpoints")
    print("=" * 50)
    
    # 1. Test User Registration
    print("\n1️⃣ Testing POST /register")
    register_data = {
        "email": "admin@test.com",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/register", json=register_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Register regular user
    user_data = {
        "email": "user@test.com", 
        "password": "user123"
    }
    requests.post(f"{BASE_URL}/register", json=user_data)
    
    # 2. Test Admin Login
    print("\n2️⃣ Testing POST /login (Admin)")
    login_response = requests.post(f"{BASE_URL}/login", json=register_data)
    print(f"Status: {login_response.status_code}")
    if login_response.status_code == 200:
        admin_token = login_response.json()["accessToken"]
        print(f"Admin Token: {admin_token[:20]}...")
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
    else:
        print("❌ Admin login failed")
        return
    
    # 3. Test User Login  
    print("\n3️⃣ Testing POST /login (User)")
    user_login = requests.post(f"{BASE_URL}/login", json=user_data)
    print(f"Status: {user_login.status_code}")
    if user_login.status_code == 200:
        user_token = user_login.json()["accessToken"]
        print(f"User Token: {user_token[:20]}...")
        user_headers = {"Authorization": f"Bearer {user_token}"}
    else:
        print("❌ User login failed")
        return
    
    # 4. Test POST /questions (Admin only)
    print("\n4️⃣ Testing POST /questions (Admin)")
    question_data = {
        "text": "What is 2+2?",
        "options": ["3", "4", "5", "6"],
        "correct_answer": "4"
    }
    response = requests.post(f"{BASE_URL}/questions", json=question_data, headers=admin_headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Add another question
    question2 = {
        "text": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "correct_answer": "Paris"
    }
    requests.post(f"{BASE_URL}/questions", json=question2, headers=admin_headers)
    
    # 5. Test GET /questions (Admin only)
    print("\n5️⃣ Testing GET /questions (Admin)")
    response = requests.get(f"{BASE_URL}/questions", headers=admin_headers)
    print(f"Status: {response.status_code}")
    questions = response.json()
    print(f"Questions count: {len(questions)}")
    
    if questions:
        question_id = questions[0]["id"]
        
        # 6. Test GET /questions/{id} (Admin only)
        print(f"\n6️⃣ Testing GET /questions/{question_id} (Admin)")
        response = requests.get(f"{BASE_URL}/questions/{question_id}", headers=admin_headers)
        print(f"Status: {response.status_code}")
        print(f"Question: {response.json()['text']}")
        
        # 7. Test PUT /questions/{id} (Admin only)
        print(f"\n7️⃣ Testing PUT /questions/{question_id} (Admin)")
        update_data = {
            "text": "What is 3+3?",
            "options": ["5", "6", "7", "8"],
            "correct_answer": "6"
        }
        response = requests.put(f"{BASE_URL}/questions/{question_id}", json=update_data, headers=admin_headers)
        print(f"Status: {response.status_code}")
        print(f"Updated: {response.json()['text']}")
    
    # 8. Test GET /quiz (User)
    print("\n8️⃣ Testing GET /quiz (User)")
    response = requests.get(f"{BASE_URL}/quiz", headers=user_headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        quiz_questions = response.json()
        print(f"Quiz questions: {len(quiz_questions)}")
        
        # 9. Test POST /quiz/result (User)
        print("\n9️⃣ Testing POST /quiz/result (User)")
        answers = {}
        for q in quiz_questions:
            answers[str(q["id"])] = q["options"][0]  # Pick first option
        
        result_data = {"answers": answers}
        response = requests.post(f"{BASE_URL}/quiz/result", json=result_data, headers=user_headers)
        print(f"Status: {response.status_code}")
        print(f"Score: {response.json()}")
    
    # 10. Test Admin access to questions (User should fail)
    print("\n🔒 Testing Admin-only access with User token")
    response = requests.get(f"{BASE_URL}/questions", headers=user_headers)
    print(f"GET /questions with user token: {response.status_code}")
    
    if questions:
        # 11. Test DELETE /questions/{id} (Admin only)
        print(f"\n🗑️ Testing DELETE /questions/{question_id} (Admin)")
        response = requests.delete(f"{BASE_URL}/questions/{question_id}", headers=admin_headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    
    print("\n✅ All endpoint tests completed!")

if __name__ == "__main__":
    try:
        test_all_endpoints()
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Start with: python -m uvicorn main:app --port 8000")