#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import logging
import pandas as pd
from typing import List, Dict, Any, Optional
import datetime

logger = logging.getLogger(__name__)

def get_csv_files(directory: str) -> List[Dict[str, Any]]:
    """
    디렉토리에서 모든 CSV 파일 목록 가져오기
    
    Args:
        directory: CSV 파일이 있는 디렉토리 경로
        
    Returns:
        CSV 파일 정보 목록 (경로, 크기, 날짜 등)
    """
    if not os.path.exists(directory):
        logger.warning(f"Directory not found: {directory}")
        return []
    
    try:
        # CSV 파일 목록 가져오기
        csv_files = glob.glob(os.path.join(directory, "*.csv"))
        
        # 파일 정보 수집
        file_info_list = []
        for file_path in csv_files:
            try:
                # 파일 기본 정보
                file_name = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                modified_time = os.path.getmtime(file_path)
                modified_time_str = datetime.datetime.fromtimestamp(modified_time).strftime("%Y-%m-%d %H:%M:%S")
                
                # CSV 파일 내용 확인
                try:
                    df = pd.read_csv(file_path, encoding='utf-8-sig', nrows=1)
                    has_evaluation = 'is_relevant' in df.columns
                except:
                    has_evaluation = False
                
                file_info = {
                    "file_name": file_name,
                    "file_path": file_path,
                    "file_size": file_size,
                    "file_size_str": format_size(file_size),
                    "modified_time": modified_time,
                    "modified_time_str": modified_time_str,
                    "has_evaluation": has_evaluation,
                    "is_evaluated": "_evaluated" in file_name
                }
                
                file_info_list.append(file_info)
            
            except Exception as e:
                logger.error(f"Error getting info for file '{file_path}': {str(e)}")
        
        # 수정 시간 기준 내림차순 정렬 (최신 파일 먼저)
        file_info_list.sort(key=lambda x: x['modified_time'], reverse=True)
        
        return file_info_list
    
    except Exception as e:
        logger.error(f"Error getting CSV files from '{directory}': {str(e)}")
        return []

def format_size(size_bytes: int) -> str:
    """
    바이트 단위 파일 크기를 읽기 쉬운 형식으로 변환
    
    Args:
        size_bytes: 바이트 단위 파일 크기
        
    Returns:
        읽기 쉬운 형식의 파일 크기 문자열
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

def get_file_content_preview(file_path: str, max_rows: int = 5) -> Dict[str, Any]:
    """
    CSV 파일 내용 미리보기
    
    Args:
        file_path: CSV 파일 경로
        max_rows: 미리 볼 최대 행 수 (기본값: 5)
        
    Returns:
        파일 내용 미리보기 정보
    """
    if not os.path.exists(file_path):
        logger.warning(f"File not found: {file_path}")
        return {"error": "File not found"}
    
    try:
        # CSV 파일 읽기
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        
        # 기본 정보
        total_rows, total_cols = df.shape
        column_names = df.columns.tolist()
        
        # 미리보기 데이터 (최대 행 수만큼)
        preview_data = df.head(max_rows).to_dict('records')
        
        return {
            "total_rows": total_rows,
            "total_columns": total_cols,
            "column_names": column_names,
            "preview_data": preview_data
        }
    
    except Exception as e:
        logger.error(f"Error getting preview for file '{file_path}': {str(e)}")
        return {"error": str(e)}

def get_file_statistics(file_path: str) -> Dict[str, Any]:
    """
    CSV 파일 통계 정보
    
    Args:
        file_path: CSV 파일 경로
        
    Returns:
        파일 통계 정보
    """
    if not os.path.exists(file_path):
        logger.warning(f"File not found: {file_path}")
        return {"error": "File not found"}
    
    try:
        # CSV 파일 읽기
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        
        # 기본 통계
        stats = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "column_names": df.columns.tolist(),
        }
        
        # 키워드 통계
        if 'keyword' in df.columns:
            keyword_counts = df['keyword'].value_counts().to_dict()
            stats["keyword_counts"] = keyword_counts
        
        # 관련성 통계
        if 'is_relevant' in df.columns:
            relevant_count = df['is_relevant'].sum()
            total_count = len(df)
            relevant_pct = relevant_count/total_count*100 if total_count > 0 else 0
            
            stats["relevant_count"] = int(relevant_count)
            stats["relevant_percent"] = round(relevant_pct, 1)
        
        # 카테고리 통계
        if 'category' in df.columns:
            category_counts = df['category'].value_counts().to_dict()
            stats["category_counts"] = category_counts
        
        return stats
    
    except Exception as e:
        logger.error(f"Error getting statistics for file '{file_path}': {str(e)}")
        return {"error": str(e)}
