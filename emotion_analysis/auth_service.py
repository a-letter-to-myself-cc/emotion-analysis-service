# import requests

# AUTH_SERVICE_URL = "http://auth-service:8001/auth"

# def verify_access_token(token: str) -> int:
#     try:
#         response = requests.post(
#             f"{AUTH_SERVICE_URL}/internal/verify/",
#             json={"token": token},
#             timeout=3
#         )
#         if response.status_code == 200:
#             return response.json().get("user_id")
#         else:
#             try:
#                 return_detail = response.json().get('detail', response.text)
#             except Exception:
#                 return_detail = response.text
#             raise Exception(f"Token verification failed: {return_detail}")
#     except requests.exceptions.RequestException as e:
#         raise Exception(f"Auth service connection failed: {str(e)}")

def verify_access_token(token: str) -> int:
    if token == "mock-token-123":
        print("✅ MOCK TOKEN 인증 통과")
        return 999
    raise Exception("❌ Invalid token (Mock mode)")
