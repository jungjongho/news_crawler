#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
import logging
from typing import List

from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/download",
    tags=["download"],
    responses={404: {"description": "File not found"}},
)


@router.get("/{file_name}")
async def download_file(file_name: str):
    """
    결과 파일 다운로드
    """
    file_path = os.path.join(settings.RESULTS_PATH, file_name)
    
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise HTTPException(status_code=404, detail=f"File '{file_name}' not found")
    
    return FileResponse(
        path=file_path, 
        filename=file_name,
        media_type="text/csv"
    )


@router.get("/zip/{folder_name}")
async def download_folder_as_zip(folder_name: str):
    """
    폴더 전체를 압축하여 다운로드
    """
    import zipfile
    import tempfile
    from datetime import datetime
    
    folder_path = os.path.join(settings.RESULTS_PATH, folder_name)
    
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        logger.error(f"Folder not found: {folder_path}")
        raise HTTPException(status_code=404, detail=f"Folder '{folder_name}' not found")
    
    # 임시 ZIP 파일 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"{folder_name}_{timestamp}.zip"
    temp_zip_path = os.path.join(tempfile.gettempdir(), zip_filename)
    
    try:
        with zipfile.ZipFile(temp_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.dirname(folder_path))
                    zipf.write(file_path, arcname)
        
        return FileResponse(
            path=temp_zip_path,
            filename=zip_filename,
            media_type="application/zip",
            background=lambda: os.remove(temp_zip_path) # 응답 후 임시 파일 삭제
        )
    
    except Exception as e:
        logger.error(f"Error creating zip file: {str(e)}")
        if os.path.exists(temp_zip_path):
            os.remove(temp_zip_path)
        raise HTTPException(status_code=500, detail=f"Error creating zip file: {str(e)}")
