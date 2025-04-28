import httpx

login_payload = {
    "email": "user@example.com",
    "password": "string"
}

login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()

assert login_response.status_code == 200
assert login_response_data['token']['accessToken'] is not None
assert login_response_data['token']['refreshToken'] is not None

access_token = login_response_data['token']['accessToken']

user_view = httpx.get("http://localhost:8000/api/v1/users/me",
                      headers={"Authorization": f"Bearer {access_token}"})
user_view_data = user_view.json()

assert user_view.status_code == 200

print(f"Response: {user_view_data}")
print(f"Status code: {user_view.status_code}")