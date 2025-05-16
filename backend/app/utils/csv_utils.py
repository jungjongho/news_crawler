#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
import json
import shutil
import datetime
from typing import List, Dict, Any, Optional, Tuple

def save_to_csv(data: List[Dict[str, Any]], file_path: str, encoding: str = 'utf-8-sig', copy_to_download: bool = False, download_path: str = None) -> Tuple[bool, Optional[str]]:
    """
    데이터를 CSV 파일로 저장합니다.
    
    Args:
        data: 저장할 데이터 리스트
        file_path: 저장할 파일 경로
        encoding: 파일 인코딩 (기본값: utf-8-sig)
        
    Returns:
        저장 성공 여부
    """
    if not data:
        return False
    
    try:
        # 디렉토리 생성
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        # 필드명 추출
        fieldnames = list(data[0].keys())
        
        # CSV 파일 저장
        with open(file_path, 'w', newline='', encoding=encoding) as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        # 다운로드 폴더에 복사
        downloaded_path = None
        if copy_to_download and download_path:
            try:
                # 다운로드 폴더 확인
                os.makedirs(download_path, exist_ok=True)
                
                # 파일명만 추출
                file_name = os.path.basename(file_path)
                download_file_path = os.path.join(download_path, file_name)
                
                # 파일 복사
                shutil.copy2(file_path, download_file_path)
                downloaded_path = download_file_path
                print(f"파일이 다운로드 폴더에 복사되었습니다: {download_file_path}")
            except Exception as e:
                print(f"다운로드 폴더 복사 중 오류: {str(e)}")
        
        return True, downloaded_path
    except Exception as e:
        print(f"CSV 저장 중 오류: {str(e)}")
        return False, None

def read_csv(file_path: str, encoding: str = 'utf-8-sig') -> List[Dict[str, Any]]:
    """
    CSV 파일에서 데이터를 읽어옵니다.
    
    Args:
        file_path: 읽을 파일 경로
        encoding: 파일 인코딩 (기본값: utf-8-sig)
        
    Returns:
        데이터 리스트
    """
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as e:
        print(f"CSV 읽기 중 오류: {str(e)}")
        return []

def get_csv_preview(file_path: str, max_rows: int = 5, encoding: str = 'utf-8-sig') -> Dict[str, Any]:
    """
    CSV 파일의 미리보기 데이터를 가져옵니다.
    
    Args:
        file_path: 파일 경로
        max_rows: 최대 행 수 (기본값: 5)
        encoding: 파일 인코딩 (기본값: utf-8-sig)
        
    Returns:
        미리보기 데이터
    """
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            column_names = reader.fieldnames or []
            
            # 최대 행 수만큼 읽기
            preview_data = []
            for i, row in enumerate(reader):
                if i >= max_rows:
                    break
                preview_data.append(row)
            
            return {
                "total_rows": get_csv_row_count(file_path),
                "total_columns": len(column_names),
                "column_names": column_names,
                "preview_data": preview_data
            }
    except Exception as e:
        print(f"CSV 미리보기 중 오류: {str(e)}")
        return {"error": str(e)}

def get_csv_row_count(file_path: str, encoding: str = 'utf-8-sig') -> int:
    """
    CSV 파일의 행 수를 계산합니다.
    
    Args:
        file_path: 파일 경로
        encoding: 파일 인코딩 (기본값: utf-8-sig)
        
    Returns:
        행 수
    """
    if not os.path.exists(file_path):
        return 0
    
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            # 헤더 제외
            reader = csv.reader(f)
            next(reader)  # 헤더 건너뛰기
            return sum(1 for _ in reader)
    except Exception:
        return 0

def get_csv_statistics(file_path: str, encoding: str = 'utf-8-sig') -> Dict[str, Any]:
    """
    CSV 파일의 통계 정보를 계산합니다.
    
    Args:
        file_path: 파일 경로
        encoding: 파일 인코딩 (기본값: utf-8-sig)
        
    Returns:
        통계 정보
    """
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    
    try:
        # CSV 파일 읽기
        data = read_csv(file_path, encoding)
        
        if not data:
            return {"error": "Empty file"}
        
        # 기본 통계
        stats = {
            "total_rows": len(data),
            "total_columns": len(data[0].keys()) if data else 0,
            "column_names": list(data[0].keys()) if data else [],
        }
        
        # 키워드 통계
        if 'keyword' in stats["column_names"]:
            keyword_counts = {}
            for row in data:
                keyword = row.get('keyword', '')
                if keyword:
                    keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
            stats["keyword_counts"] = keyword_counts
        
        # 관련성 통계
        if 'is_relevant' in stats["column_names"]:
            relevant_count = sum(1 for row in data if str(row.get('is_relevant', '')).lower() in ['true', '1', 'yes'])
            stats["relevant_count"] = relevant_count
            stats["relevant_percent"] = round((relevant_count / len(data)) * 100, 1) if data else 0
        
        # 카테고리 통계
        if 'category' in stats["column_names"]:
            category_counts = {}
            for row in data:
                category = row.get('category', '')
                if category:
                    category_counts[category] = category_counts.get(category, 0) + 1
            stats["category_counts"] = category_counts
        
        return stats
    except Exception as e:
        print(f"CSV 통계 계산 중 오류: {str(e)}")
        return {"error": str(e)}

def get_csv_files(directory: str) -> List[Dict[str, Any]]:
    """
    디렉토리에서 모든 CSV 파일 목록을 가져옵니다.
    
    Args:
        directory: CSV 파일이 있는 디렉토리 경로
        
    Returns:
        CSV 파일 정보 목록
    """
    if not os.path.exists(directory):
        return []
    
    try:
        # CSV 파일 목록 가져오기
        file_info_list = []
        for file_name in os.listdir(directory):
            if file_name.endswith('.csv'):
                file_path = os.path.join(directory, file_name)
                
                # 파일 기본 정보
                stat = os.stat(file_path)
                modified_time = stat.st_mtime
                modified_time_str = datetime.datetime.fromtimestamp(modified_time).strftime("%Y-%m-%d %H:%M:%S")
                
                # CSV 파일 내용 확인
                has_evaluation = False
                try:
                    with open(file_path, 'r', encoding='utf-8-sig') as f:
                        header = next(csv.reader(f))
                        has_evaluation = 'is_relevant' in header
                except:
                    pass
                
                file_info = {
                    "file_name": file_name,
                    "file_path": file_path,
                    "file_size": stat.st_size,
                    "file_size_str": format_size(stat.st_size),
                    "modified_time": modified_time,
                    "modified_time_str": modified_time_str,
                    "has_evaluation": has_evaluation,
                    "is_evaluated": "_evaluated" in file_name
                }
                
                file_info_list.append(file_info)
        
        # 수정 시간 기준 내림차순 정렬 (최신 파일 먼저)
        file_info_list.sort(key=lambda x: x['modified_time'], reverse=True)
        
        return file_info_list
    except Exception as e:
        print(f"파일 목록 가져오기 중 오류: {str(e)}")
        return []

def format_size(size_bytes: int) -> str:
    """
    바이트 단위 파일 크기를 읽기 쉬운 형식으로 변환합니다.
    
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
