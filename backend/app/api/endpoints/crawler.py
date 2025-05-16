#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Response
from typing import List, Dict, Any, Optional
import logging
import os

from app.models.schemas import CrawlerRequest, CrawlerResponse, FileListResponse, DownloadLinkResponse
from app.services.crawler_service import CrawlerService
from app.utils.csv_utils import get_csv_files, get_csv_preview, get_csv_statistics
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/crawler",
    tags=["crawler"],
    responses={404: {"description": "Not found"}},
)

# CrawlerService 인스턴스 생성 함수
def get_crawler_service() -> CrawlerService:
    return CrawlerService()

@router.post("/crawl", response_model=CrawlerResponse)
async def crawl_news(
    request: CrawlerRequest,
    background_tasks: BackgroundTasks,
    crawler_service: CrawlerService = Depends(get_crawler_service)
):
    """
    키워드 목록에 대한 뉴스 크롤링
    """
    logger.info(f"Crawling news for keywords: {request.keywords}")
    
    try:
        # 크롤링 실행
        news_items, errors = crawler_service.crawl_keywords(
            request.keywords, 
            request.max_news_per_keyword
        )
        
        if not news_items:
            return CrawlerResponse(
                success=False,
                message="No news items found for the given keywords",
                errors=errors
            )
        
        # 결과 저장
        file_path, download_path = crawler_service.save_results(news_items)
        
        if not file_path:
            return CrawlerResponse(
                success=False,
                message="Failed to save crawler results",
                errors={"save_error": "Could not save results to file"}
            )
        
        # 상대 경로로 변환
        rel_path = os.path.relpath(file_path, os.path.dirname(settings.RESULTS_PATH))
        
        # 다운로드 폴더 저장 결과 추가
        message = f"Successfully crawled {len(news_items)} news items"
        if download_path:
            message += f" and saved to your Downloads folder: {os.path.basename(download_path)}"
        
        return CrawlerResponse(
            success=True,
            message=message,
            file_path=rel_path,
            item_count=len(news_items),
            keywords=request.keywords,
            download_path=download_path if download_path else None,
            errors=errors if errors else None
        )
    
    except Exception as e:
        logger.error(f"Error during crawling: {str(e)}")
        return CrawlerResponse(
            success=False,
            message=f"Error during crawling: {str(e)}",
            errors={"crawling_error": str(e)}
        )

@router.get("/files", response_model=FileListResponse)
async def get_files():
    """
    크롤링 결과 파일 목록 조회
    """
    files = get_csv_files(settings.RESULTS_PATH)
    return FileListResponse(files=files)

@router.get("/files/{file_name}/preview")
async def get_file_preview(file_name: str, max_rows: int = 5):
    """
    파일 내용 미리보기
    """
    file_path = os.path.join(settings.RESULTS_PATH, file_name)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File '{file_name}' not found")
    
    preview = get_csv_preview(file_path, max_rows)
    
    if "error" in preview:
        raise HTTPException(status_code=500, detail=preview["error"])
    
    return preview

@router.get("/files/{file_name}/statistics")
async def get_file_stats(file_name: str):
    """
    파일 통계 정보
    """
    file_path = os.path.join(settings.RESULTS_PATH, file_name)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File '{file_name}' not found")
    
    stats = get_csv_statistics(file_path)
    
    if "error" in stats:
        raise HTTPException(status_code=500, detail=stats["error"])
    
    return stats


@router.get("/files/{file_name}/download-link", response_model=DownloadLinkResponse)
async def get_file_download_link(file_name: str):
    """
    파일 다운로드 링크 생성
    """
    file_path = os.path.join(settings.RESULTS_PATH, file_name)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File '{file_name}' not found")
    
    download_link = f"/api/download/{file_name}"
    
    return DownloadLinkResponse(
        success=True,
        download_link=download_link,
        file_name=file_name
    )
