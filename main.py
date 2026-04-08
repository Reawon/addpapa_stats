import time
import hmac
import hashlib
import base64
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 네이버 API 설정 (여기에 본인의 키를 입력하세요)
CUSTOMER_ID = "4347190"
ACCESS_KEY = "010000000059d5664ef1871c59c737fcd934ce1f7272f8021661bc5504b5aef942e68b014e"
SECRET_KEY = "AQAAAABZ1WZO8YccWcc3/Nk0zh9yD5h9HFeMJHwv2BXw/IeqhQ=="

def generate_signature(timestamp, method, uri, secret_key):
    message = f"{timestamp}.{method}.{uri}"
    hash = hmac.new(secret_key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256)
    return base64.b64encode(hash.digest()).decode("utf-8")

@app.get("/stats/{keyword}")
def get_naver_stats(keyword: str):
    timestamp = str(int(time.time() * 1000))
    uri = "/keywordstool"
    method = "GET"
    
    signature = generate_signature(timestamp, method, uri, SECRET_KEY)
    
    headers = {
        "X-Timestamp": timestamp,
        "X-API-KEY": ACCESS_KEY,
        "X-Customer": CUSTOMER_ID,
        "X-Signature": signature,
    }
    
    params = {"hintKeywords": keyword, "showDetail": "1"}
    
    response = requests.get(f"https://naver.com{uri}", params=params, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        # json 에러가 나기 전에 원시 텍스트 응답을 직접 확인합니다.
        return {
            "status_code": response.status_code,
            "error_message": response.text,  # <--- 여기서 진짜 원인이 보일 거예요
            "sent_headers": {
                "X-Timestamp": timestamp,
                "X-API-KEY": ACCESS_KEY,
                "X-Customer": CUSTOMER_ID
            }
        }
