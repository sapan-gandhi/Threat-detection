import requests
import json
import time

BASE_URL = "http://localhost:8000"
USER_EMAIL = "test_e2e_user@spamshield.com"
ADMIN_EMAIL = "admin@spamshield.com"

def run_tests():
    print("--- Starting End-to-End Verification ---")
    
    # 1. Test Login/Registration
    print("\n1. Testing User Registration/Login...")
    res = requests.post(f"{BASE_URL}/auth/register", json={"email": USER_EMAIL, "name": "E2E User", "password": "password"})
    if res.status_code == 400 and "already registered" in res.text:
        # User exists, just login
        res = requests.post(f"{BASE_URL}/auth/login", json={"email": USER_EMAIL, "password": "password"})
    
    assert res.status_code == 200, f"Auth failed: {res.text}"
    user_data = res.json()
    user_id = user_data["id"]
    print(f"✅ Login successful! User ID: {user_id}")

    # 2. Test ML Model - Safe Message
    print("\n2. Testing ML Model (Safe Message)...")
    safe_msg = {"content": "Hey, are we still meeting for lunch tomorrow at 12?", "msg_type": "sms"}
    res = requests.post(f"{BASE_URL}/api/messages/analyze?user_id={user_id}", json=safe_msg)
    assert res.status_code == 200, f"Analysis failed: {res.text}"
    safe_res = res.json()
    print(f"   Prediction: {safe_res['prediction']} (Confidence: {safe_res['confidence']:.2f})")
    assert safe_res['prediction'] == "Safe", "Model incorrectly classified safe message!"
    print("✅ ML Safe classification passed!")
    safe_msg_id = safe_res["id"]

    # 3. Test ML Model - Spam Message
    print("\n3. Testing ML Model (Spam Message)...")
    spam_msg = {"content": "URGENT! You have won a $1000 Walmart gift card. Click here to claim your prize now: http://fake-spam-link.com", "msg_type": "email"}
    res = requests.post(f"{BASE_URL}/api/messages/analyze?user_id={user_id}", json=spam_msg)
    assert res.status_code == 200, f"Analysis failed: {res.text}"
    spam_res = res.json()
    print(f"   Prediction: {spam_res['prediction']} (Confidence: {spam_res['confidence']:.2f})")
    assert spam_res['prediction'] == "Spam", "Model incorrectly classified spam message!"
    print("✅ ML Spam classification passed!")

    # 4. Test User Dashboard Stats (Database Verification)
    print("\n4. Testing User Dashboard Stats...")
    res = requests.get(f"{BASE_URL}/api/dashboard/stats?user_id={user_id}")
    assert res.status_code == 200, f"Dashboard stats failed: {res.text}"
    stats = res.json()
    print(f"   Total Analyzed: {stats['total_analyzed']}, Spam: {stats['spam_detected']}")
    # Assert at least the ones we just created are there
    assert stats['total_analyzed'] >= 2, "Database did not properly store new messages!"
    print("✅ Database storage and stats aggregation passed!")

    # 5. Test Message Deletion
    print("\n5. Testing Message Deletion...")
    res = requests.delete(f"{BASE_URL}/api/messages/{safe_msg_id}?user_id={user_id}")
    assert res.status_code == 200, f"Deletion failed: {res.text}"
    print("✅ Message successfully deleted from database!")

    # 6. Test Admin Login
    print("\n6. Testing Admin Login...")
    res = requests.post(f"{BASE_URL}/auth/admin/login", json={"email": ADMIN_EMAIL, "password": "admin123"})
    assert res.status_code == 200, f"Admin login failed: {res.text}"
    print("✅ Admin login successful!")

    # 7. Test Admin Dashboard Stats
    print("\n7. Testing Admin Dashboard Stats...")
    res = requests.get(f"{BASE_URL}/api/admin/dashboard-stats")
    assert res.status_code == 200, f"Admin dashboard stats failed: {res.text}"
    admin_dash = res.json()
    print(f"   Total Users in DB: {admin_dash['total_users']}")
    assert admin_dash['total_users'] > 0, "No users found in admin stats!"
    print("✅ Admin statistics fetching passed!")

    print("\n--- ✅ ALL END-TO-END TESTS PASSED SUCCESSFULLY! ---")

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
