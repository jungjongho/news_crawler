#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Settings(BaseSettings):
    # API 기본 설정
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "네이버 뉴스 스크래퍼"
    
    # CORS 설정
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # OpenAI API 설정
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", "")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")
    
    # 스크래핑 설정
    DEFAULT_KEYWORD_LIST: List[str] = [
        "코스맥스", "코스맥스엔비티", "콜마", "HK이노엔", 
        "아모레퍼시픽", "LG생활건강", "올리브영", "화장품", "뷰티",
        "건강기능식품", "펫푸드", "마이크로바이옴", "식품의약품안전처"
    ]
    
    # 검색 결과 저장 경로
    RESULTS_PATH: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "results")
    
    # 사용자 다운로드 폴더 경로
    @property
    def USER_DOWNLOAD_PATH(self) -> str:
        if platform.system() == "Windows":
            return os.path.join(os.path.expanduser("~"), "Downloads")
        elif platform.system() == "Darwin":  # macOS
            return os.path.join(os.path.expanduser("~"), "Downloads")
        else:  # Linux, etc.
            return os.path.join(os.path.expanduser("~"), "Downloads")
    
    # 결과 파일을 사용자 다운로드 폴더에 자동으로 복사할지 여부
    AUTO_COPY_TO_DOWNLOADS: bool = True
    
    # 기타 설정
    MAX_NEWS_PER_KEYWORD: int = 100
    
    model_config = SettingsConfigDict(case_sensitive=True)

settings = Settings()
