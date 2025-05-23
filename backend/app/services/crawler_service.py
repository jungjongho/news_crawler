#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
# import pandas as pd
from app.utils.csv_utils import save_to_csv, save_to_excel
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import logging
import datetime
from typing import List, Dict, Any, Optional, Tuple

from app.utils.naver_news_helper import (
    extract_news_items, extract_title, extract_url, 
    extract_source, extract_date, extract_content
)
from app.core.config import settings

logger = logging.getLogger(__name__)

class CrawlerService:
    """
    네이버 뉴스 크롤링 서비스
    """
    def __init__(self):
        """
        서비스 초기화
        """
        self.base_url = "https://search.naver.com/search.naver"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # 결과 저장 디렉토리 확인 및 생성
        os.makedirs(settings.RESULTS_PATH, exist_ok=True)
    
    def _build_search_url(self, keyword: str, start_page: int = 1) -> str:
        """
        검색 URL 생성
        
        Args:
            keyword: 검색 키워드
            start_page: 시작 페이지 (기본값: 1)
            
        Returns:
            생성된 검색 URL
        """
        # 기본 파라미터: 뉴스 검색, 최신순 정렬 (2025년 5월 기준 최신 URL 형식)
        params = {
            'ssc': 'tab.news.all',
            'query': keyword,
            'sm': 'tab_opt',
            'sort': 1,  # 최신순
            'photo': 0,
            'field': 0,
            'pd': -1,   # 전체 기간
            'ds': '',
            'de': '',
            'docid': '',
            'related': 0,
            'mynews': 0,
            'office_type': 0,
            'office_section_code': 0,
            'news_office_checked': '',
            'nso': 'so:dd,p:all',  # 최신순, 전체 기간
            'is_sug_officeid': 0,
            'start': (start_page - 1) * 10 + 1  # 페이지네이션
        }
        
        # URL 파라미터 생성
        param_str = "&".join([f"{k}={quote_plus(str(v)) if k == 'query' else v}" for k, v in params.items()])
        return f"{self.base_url}?{param_str}"
    
    def _format_keywords_for_filename(self, news_items: List[Dict[str, Any]]) -> str:
        """
        뉴스 아이템에서 키워드를 추출하여 파일명에 적합한 형식으로 변환
        
        Args:
            news_items: 뉴스 아이템 목록
            
        Returns:
            파일명에 사용할 키워드 문자열
        """
        # 모든 고유한 키워드 추출
        unique_keywords = set()
        for item in news_items:
            keyword = item.get('keyword', '')
            if keyword:
                unique_keywords.add(keyword)
        
        # 파일이름에 적합한 형태로 변환
        # 길이 제한 (너무 길면 파일 경로 문제 발생 가능)
        if len(unique_keywords) > 3:
            # 3개 이상이면 처음 3개만 유지하고 나머지는 개수 표시
            sorted_keywords = sorted(list(unique_keywords))[:3]
            keywords_str = '_'.join(sorted_keywords) + f"_and_{len(unique_keywords)-3}_more"
        else:
            # 3개 이하면 모두 포함
            keywords_str = '_'.join(sorted(list(unique_keywords)))
        
        # 파일명에 사용할 수 없는 문자 제거
        keywords_str = keywords_str.replace(' ', '_').replace('/', '_').replace('\\', '_')
        # 최대 길이 제한
        if len(keywords_str) > 100:  # 적절한 최대 길이
            keywords_str = keywords_str[:97] + '...'
        
        return keywords_str
    
    def crawl_keyword(self, keyword: str, max_news: int = 50) -> List[Dict[str, Any]]:
        """
        특정 키워드에 대한 뉴스 크롤링
        
        Args:
            keyword: 검색 키워드
            max_news: 최대 뉴스 건수 (기본값: 50)
            
        Returns:
            크롤링한 뉴스 아이템 목록
        """
        logger.info(f"Crawling news for keyword: {keyword}, max_news: {max_news}")
        news_items = []
        page = 1
        
        while len(news_items) < max_news:
            try:
                # 검색 URL 생성 및 요청
                url = self._build_search_url(keyword, page)
                logger.info(f"Requesting URL: {url}")
                
                # URL 로그 기록 기능 제거됨
                
                response = requests.get(url, headers=self.headers)
                if response.status_code != 200:
                    logger.error(f"Failed to fetch page {page} for keyword '{keyword}': {response.status_code}")
                    logger.error(f"Response content: {response.text[:500]}")
                    
                    # 오류 로그 기록 기능 제거됨
                    
                    break
                
                # HTML 파싱
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 디버그용 - HTML 구조 파악
                logger.info(f"HTML Content Length: {len(response.text)}")
                logger.debug(f"First 1000 chars of HTML: {response.text[:1000]}")
                
                # HTML 저장 기능 제거됨
                
                # CSS 선택자 확인
                ul_element = soup.select_one('ul.list_news._infinite_list')
                if ul_element:
                    logger.info("Found list_news._infinite_list element")
                    logger.debug(f"First ul element: {str(ul_element)[:500]}")
                
                # 뉴스 아이템 추출
                items = extract_news_items(soup)
                
                if not items:
                    logger.warning(f"No news items found on page {page} for keyword '{keyword}'")
                    break
                
                # 각 뉴스 항목 처리
                for item in items:
                    if len(news_items) >= max_news:
                        break
                    
                    title = extract_title(item)
                    url = extract_url(item)
                    source = extract_source(item)
                    date = extract_date(item)
                    content = extract_content(item)
                    
                    # 유효한 항목만 추가
                    if title and url:
                        news_items.append({
                            'title': title,
                            'url': url,
                            'source': source,
                            'date': date,
                            'content': content,
                            'keyword': keyword
                        })
                
                # 다음 페이지로 이동
                page += 1
                
                # 더 이상 결과가 없으면 중단
                if len(items) < 10:
                    logger.info(f"End of results reached for keyword '{keyword}' at page {page}")
                    break
                
                # 최대 20페이지까지만 검색 (네이버 최대 페이지 제한)
                if page > 20:
                    logger.info(f"Maximum page limit reached for keyword '{keyword}'")
                    break
                
            except Exception as e:
                logger.error(f"Error crawling page {page} for keyword '{keyword}': {str(e)}")
                break
        
        logger.info(f"Crawled {len(news_items)} news items for keyword '{keyword}'")
        return news_items
    
    def crawl_keywords(self, keywords: List[str], max_news_per_keyword: int = 50) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
        """
        여러 키워드에 대한 뉴스 크롤링
        
        Args:
            keywords: 검색 키워드 목록
            max_news_per_keyword: 키워드당 최대 뉴스 건수 (기본값: 50)
            
        Returns:
            (크롤링한 뉴스 아이템 목록, 오류 정보)
        """
        all_news_items = []
        errors = {}
        
        for keyword in keywords:
            try:
                news_items = self.crawl_keyword(keyword, max_news_per_keyword)
                all_news_items.extend(news_items)
            except Exception as e:
                logger.error(f"Error crawling keyword '{keyword}': {str(e)}")
                errors[keyword] = str(e)
        
        logger.info(f"Crawled total of {len(all_news_items)} news items for {len(keywords)} keywords")
        return all_news_items, errors
    
    def save_results(self, news_items: List[Dict[str, Any]]) -> Tuple[Optional[str], Optional[str]]:
        """
        크롤링 결과를 CSV 파일로 저장
        
        Args:
            news_items: 저장할 뉴스 아이템 목록
            
        Returns:
            (저장된 파일 경로, 다운로드 폴더에 저장된 파일 경로) 또는 오류 시 (None, None)
        """
        if not news_items:
            logger.warning("No news items to save")
            return None, None
        
        try:
            # 파일명 생성 (키워드와 현재 시간 포함)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 키워드 추출 및 포맷팅
            keywords_str = self._format_keywords_for_filename(news_items)
            
            file_name = f"naver_news_{keywords_str}_{timestamp}.csv"
            file_path = os.path.join(settings.RESULTS_PATH, file_name)
            
            # CSV 파일로 저장 (다운로드 폴더에도 복사)
            success, download_path = save_to_csv(
                news_items, 
                file_path, 
                encoding='utf-8-sig',
                copy_to_download=settings.AUTO_COPY_TO_DOWNLOADS,
                download_path=settings.USER_DOWNLOAD_PATH
            )
            
            if success:
                if download_path:
                    logger.info(f"Saved {len(news_items)} news items to {file_path} and copied to {download_path}")
                else:
                    logger.info(f"Saved {len(news_items)} news items to {file_path}")
                return file_path, download_path
            else:
                logger.error("Failed to save results")
                return None, None
        
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
            return None, None
            
    def save_results_to_excel(self, news_items: List[Dict[str, Any]]) -> Tuple[Optional[str], Optional[str]]:
        """
        크롤링 결과를 Excel 파일로 저장
        
        Args:
            news_items: 저장할 뉴스 아이템 목록
            
        Returns:
            (저장된 파일 경로, 다운로드 폴더에 저장된 파일 경로) 또는 오류 시 (None, None)
        """
        if not news_items:
            logger.warning("No news items to save")
            return None, None
        
        try:
            # 파일명 생성 (키워드와 현재 시간 포함)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 키워드 추출 및 포맷팅
            keywords_str = self._format_keywords_for_filename(news_items)
            
            file_name = f"naver_news_{keywords_str}_{timestamp}.xlsx"
            file_path = os.path.join(settings.RESULTS_PATH, file_name)
            
            # Excel 파일로 저장 (다운로드 폴더에도 복사)
            success, download_path = save_to_excel(
                news_items, 
                file_path,
                copy_to_download=settings.AUTO_COPY_TO_DOWNLOADS,
                download_path=settings.USER_DOWNLOAD_PATH
            )
            
            if success:
                if download_path:
                    logger.info(f"Saved {len(news_items)} news items to Excel file {file_path} and copied to {download_path}")
                else:
                    logger.info(f"Saved {len(news_items)} news items to Excel file {file_path}")
                return file_path, download_path
            else:
                logger.error("Failed to save results to Excel")
                return None, None
        
        except Exception as e:
            logger.error(f"Error saving results to Excel: {str(e)}")
            return None, None
