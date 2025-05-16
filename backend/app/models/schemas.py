#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class NewsItem(BaseModel):
    """
    단일 뉴스 아이템을 나타내는 스키마
    """
    title: str
    content: str
    date: str
    source: str
    url: str
    keyword: str
    is_relevant: Optional[bool] = False
    relevance_reason: Optional[str] = ""
    category: Optional[str] = "기타"
    highlights: Optional[List[str]] = []


class CrawlerRequest(BaseModel):
    """
    뉴스 크롤링 요청 스키마
    """
    keywords: List[str] = Field(..., description="검색할 키워드 목록")
    max_news_per_keyword: Optional[int] = Field(50, description="키워드당 최대 뉴스 건수")


class CrawlerResponse(BaseModel):
    """
    뉴스 크롤링 응답 스키마
    """
    success: bool = Field(..., description="크롤링 성공 여부")
    message: str = Field(..., description="응답 메시지")
    file_path: Optional[str] = Field(None, description="결과 파일 경로")
    download_path: Optional[str] = Field(None, description="다운로드 폴더에 저장된 파일 경로")
    item_count: Optional[int] = Field(None, description="총 뉴스 항목 수")
    keywords: Optional[List[str]] = Field(None, description="검색한 키워드 목록")
    errors: Optional[Dict[str, str]] = Field(None, description="오류 정보")


class RelevanceRequest(BaseModel):
    """
    관련성 평가 요청 스키마
    """
    file_path: str = Field(..., description="평가할 CSV 파일 경로")
    api_key: str = Field(..., description="OpenAI 또는 Claude API 키")
    model: Optional[str] = Field("gpt-3.5-turbo", description="사용할 LLM 모델")


class RelevanceResponse(BaseModel):
    """
    관련성 평가 응답 스키마
    """
    success: bool = Field(..., description="평가 성공 여부")
    message: str = Field(..., description="응답 메시지")
    file_path: Optional[str] = Field(None, description="결과 파일 경로")
    stats: Optional[Dict[str, Any]] = Field(None, description="평가 통계 정보")
    errors: Optional[Dict[str, str]] = Field(None, description="오류 정보")


class FileListResponse(BaseModel):
    """
    파일 목록 응답 스키마
    """
    files: List[Dict[str, Any]] = Field(..., description="파일 목록 (경로, 크기, 날짜 등)")


class EmailRequest(BaseModel):
    """
    이메일 전송 요청 스키마
    """
    recipients: List[str] = Field(..., description="수신자 이메일 주소 목록")
    subject: Optional[str] = Field("네이버 뉴스 스크래핑 결과", description="이메일 제목")
    file_path: str = Field(..., description="첨부할 파일 경로")
    message: Optional[str] = Field("첨부된 파일에 뉴스 스크래핑 결과가 있습니다.", description="이메일 본문")


class DownloadLinkResponse(BaseModel):
    """
    파일 다운로드 링크 응답 스키마
    """
    success: bool = Field(..., description="성공 여부")
    download_link: str = Field(..., description="다운로드 링크")
    file_name: str = Field(..., description="파일명")
