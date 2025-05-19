from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uvicorn

from crawler import NaverNewsCrawler
from models import NewsItem

app = FastAPI(title="뉴스 크롤러 API", description="네이버 뉴스 크롤링 API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 구체적인 도메인 지정 필요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "뉴스 크롤러 API에 오신 것을 환영합니다"}

@app.get("/api/news/{keyword}", response_model=List[NewsItem])
async def get_news(keyword: str, limit: Optional[int] = 10):
    """
    키워드로 네이버 뉴스를 검색하고 결과를 반환합니다.
    """
    try:
        crawler = NaverNewsCrawler()
        news_items = crawler.crawl_news(keyword, limit)
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
