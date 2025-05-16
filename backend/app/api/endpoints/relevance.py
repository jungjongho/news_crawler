#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List, Dict, Any, Optional
import logging
import os

from app.models.schemas import RelevanceRequest, RelevanceResponse
from app.services.relevance_service import RelevanceService
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/relevance",
    tags=["relevance"],
    responses={404: {"description": "Not found"}},
)

# RelevanceService 인스턴스 생성 함수
def get_relevance_service(api_key: str, model: str) -> RelevanceService:
    return RelevanceService(api_key=api_key, model=model)

@router.post("/evaluate", response_model=RelevanceResponse)
async def evaluate_news(
    request: RelevanceRequest,
    background_tasks: BackgroundTasks
):
    """
    CSV 파일에 있는 뉴스 기사 관련성 평가
    """
    logger.info(f"Evaluating relevance for file: {request.file_path}")
    
    # 절대 경로 또는 상대 경로 처리
    if not os.path.isabs(request.file_path):
        file_path = os.path.join(settings.RESULTS_PATH, request.file_path)
    else:
        file_path = request.file_path
    
    if not os.path.exists(file_path):
        return RelevanceResponse(
            success=False,
            message=f"File not found: {request.file_path}",
            errors={"file_error": "File not found"}
        )
    
    try:
        # 관련성 평가 서비스 생성
        relevance_service = get_relevance_service(request.api_key, request.model)
        
        # 파일 처리 및 관련성 평가 실행
        output_file, stats = relevance_service.process_file(file_path)
        
        if not output_file:
            return RelevanceResponse(
                success=False,
                message="Failed to process file for relevance evaluation",
                errors=stats.get("error", {"process_error": "Unknown error"})
            )
        
        # 상대 경로로 변환
        rel_path = os.path.relpath(output_file, os.path.dirname(settings.RESULTS_PATH))
        
        return RelevanceResponse(
            success=True,
            message=f"Successfully evaluated relevance for file: {os.path.basename(request.file_path)}",
            file_path=rel_path,
            stats=stats
        )
    
    except Exception as e:
        logger.error(f"Error during relevance evaluation: {str(e)}")
        return RelevanceResponse(
            success=False,
            message=f"Error during relevance evaluation: {str(e)}",
            errors={"evaluation_error": str(e)}
        )
