#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import sys
import logging
from typing import List

from app.api.endpoints import crawler, relevance, download
from app.core.config import settings

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# 결과 디렉토리 생성
results_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')
os.makedirs(results_dir, exist_ok=True)

app = FastAPI(
    title="네이버 뉴스 스크래퍼 API",
    description="네이버 뉴스 검색 및 스크래핑을 위한 API",
    version="1.0.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 오리진 허용 (개발 환경)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 설정
app.include_router(crawler.router)
app.include_router(relevance.router)
app.include_router(download.router)

# 결과 파일 정적 호스팅
app.mount("/results", StaticFiles(directory=results_dir), name="results")

@app.get("/")
async def root():
    return {"message": "네이버 뉴스 스크래퍼 API에 오신 것을 환영합니다!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
