from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 프론트엔드(addpapa.com)에서 접속할 수 있게 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 테스트용으로 모두 허용, 나중에 도메인으로 제한
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Addpapa 통계 서버가 작동 중입니다!!"}

@app.get("/stats/{keyword}")
def get_stats(keyword: str):
    # 나중에 여기에 네이버 API 연동 로직이 들어갑니다.
    return {
        "keyword": keyword,
        "monthly_search_volume": 1250, # 임시 데이터
        "status": "success"
    }
