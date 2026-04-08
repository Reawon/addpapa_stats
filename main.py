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

# 이미지에 표시된 정보를 정확히 입력하세요
CUSTOMER_ID = "4347190"
ACCESS_KEY = "010000000059d5664ef1871c59c737fcd934ce1f7272f8021661bc5504b5aef942e68b014e"
SECRET_KEY = "AQAAAABZ1WZO8YccWcc3/Nk0zh9yD5h9HFeMJHwv2BXw/IeqhQ=="

def generate_signature(timestamp, method, uri, secret_key):
    # 네이버 API 가이드에 따른 정확한 서명 생성 포맷
    message = f"{timestamp}.{method}.{uri}"
    hash = hmac.new(secret_key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256)
    return base64.b64encode(hash.digest()).decode("utf-8")

@app.get("/naver/{keyword}")
def get_naver_stats(keyword: str):
    timestamp = str(int(time.time() * 1000))
    uri = "/keywordstool" # 서명 생성 시에는 쿼리 스트링을 제외한 순수 경로만 사용
    method = "GET"
    
    signature = generate_signature(timestamp, method, uri, SECRET_KEY)
    
    headers = {
        "X-Timestamp": timestamp,
        "X-API-KEY": ACCESS_KEY,
        "X-Customer": CUSTOMER_ID,
        "X-Signature": signature,
    }
    
    # 실제 요청 시에는 파라미터를 명확히 분리하여 전달
    params = {
        "hintKeywords": keyword,
        "showDetail": "1"
    }
    
    try:
        # 네이버 API 정식 주소: https://naver.com
        response = requests.get("https://api.searchad.naver.com/keywordstool", params=params, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status_code": response.status_code,
                "error_detail": response.text, # 에러 원인을 텍스트로 바로 확인
                "keyword": keyword
            }
    except Exception as e:
        return {"error": "시스템 오류", "message": str(e)}

# 구글 통계 기능은 아직 준비 중입니다. 추후 업데이트 예정입니다.
@app.get("/google/{keyword}")
def get_google_stats(keyword: str):

    return {
        "source": "google",
        "keyword": keyword,
        "message": "구글 통계 기능은 준비 중입니다! (Coming Soon)"
    }