#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
네이버 뉴스 크롤링 헬퍼 함수
네이버 뉴스 검색 결과 페이지의 구조가 자주 변경될 수 있으므로, 
여러 가지 CSS 선택자를 시도하여 필요한 정보를 추출하는 헬퍼 함수 모음
"""

from bs4 import BeautifulSoup
import re
import logging

logger = logging.getLogger(__name__)

def extract_news_items(soup):
    """
    뉴스 아이템 목록을 추출하는 함수
    다양한 선택자를 순차적으로 시도
    """
    # 2025년 5월 최신 구조 (with debug info)
    logger.debug(f"Soup content (first 500 chars): {str(soup)[:500]}")
    
    # 원본 HTML 구조에서 추출한 선택자
    items = soup.select('div.sds-comps-vertical-layout.sds-comps-full-layout.iYo99IP8GixD0iM_4cb8')
    if items:
        logger.info(f"News items found using 2025 May selector (vertical layout), count: {len(items)}")
        return items
        
    # 전체 기사 기본 이미지
    items = soup.select('div.sds-comps-vertical-layout.sds-comps-full-layout._ZFrFZ37i2aIyKHzNWlA')
    if items:
        logger.info(f"News items found using 2025 May selector (_ZFrFZ37i2aIyKHzNWlA), count: {len(items)}")
        return items
        
    # 2025년 5월 구조 (Xpath 및 선택자 정보 기반)
    items = soup.select('#main_pack > section > div > div > ul > li')
    if items:
        logger.info(f"News items found using latest 2025 May selector (xpath), count: {len(items)}")
        return items
    
    # 2025년 5월 구조 (ul 리스트 기반)
    items = soup.select('ul.list_news._infinite_list li')
    if items:
        logger.info(f"News items found using 2025 May selector (list_news), count: {len(items)}")
        return items
        
    # 다른 가능한 선택자들
    selectors = [
        'div.group_news > ul.list_news > li',
        'ul.list_news > li',
        'div.news_wrap.api_ani_send',
        'div.news_area',
        'div.newsitem',
        'li.bx',
        '#main_pack > section > div > div > ul > li'
    ]
    for selector in selectors:
        items = soup.select(selector)
        if items:
            logger.info(f"News items found using selector: {selector}, count: {len(items)}")
            return items
    
    # 모든 선택자가 실패한 경우 빈 리스트 반환
    logger.warning("No news items found with any selectors")
    return []

def extract_title(item):
    """
    뉴스 아이템에서 제목을 추출하는 함수
    """
    # 2025년 5월 최신 구조 (제공된 HTML 정보 기반)
    title_element = item.select_one('a.X0fMYp2dHd0TCUS2hjww.OgU1CD78f4cPaKGs1OeY span.sds-comps-text-ellipsis-1.sds-comps-text-type-headline1')
    if title_element:
        return title_element.get_text(strip=True)
    
    # 2025년 5월 구조 (다른 가능한 클래스)
    title_element = item.select_one('a.X0fMYp2dHd0TCUS2hjww span.sds-comps-text-ellipsis-1.sds-comps-text-type-headline1')
    if title_element:
        return title_element.get_text(strip=True)

    # 더 간단한 선택자로 시도
    title_element = item.select_one('span.sds-comps-text-ellipsis-1.sds-comps-text-type-headline1')
    if title_element:
        return title_element.get_text(strip=True)
    
    # 다른 가능한 선택자들
    selectors = [
        'a.news_tit',
        'div.news_area a.news_tit',
        'div.news_wrap a.news_tit',
        'a.api_txt_lines.api_txt_lines_title',
        'div.news_contents h2.news_title',
        'div.newslist_item a.newslist_item_title',
        'div.news_area div.news_wrap a.news_tit'
    ]
    
    for selector in selectors:
        title_element = item.select_one(selector)
        if title_element:
            return title_element.get_text(strip=True)
    
    # 모든 선택자가 실패한 경우, 제목 포함 가능성이 있는 모든 텍스트 노드 확인
    for tag in item.find_all(['h2', 'h3', 'h4', 'strong', 'a']):
        if tag.get_text(strip=True) and len(tag.get_text(strip=True)) > 10:
            return tag.get_text(strip=True)
    
    return "제목 없음"

def extract_url(item):
    """
    뉴스 아이템에서 URL을 추출하는 함수
    """
    # 2025년 5월 최신 구조
    url_element = item.select_one('a.X0fMYp2dHd0TCUS2hjww.OgU1CD78f4cPaKGs1OeY')
    if url_element and url_element.has_attr('href'):
        return url_element.get('href')
        
    # 유사한 선택자 시도 
    url_element = item.select_one('a.X0fMYp2dHd0TCUS2hjww')
    if url_element and url_element.has_attr('href'):
        return url_element.get('href')
    
    # 다른 가능한 선택자들
    selectors = [
        'a.news_tit',
        'div.news_area a.news_tit',
        'div.news_wrap a.news_tit',
        'a.api_txt_lines.api_txt_lines_title',
        'div.news_info_group a.urlBtn',
        'div.news_contents a.news_source_link'
    ]
    
    for selector in selectors:
        url_element = item.select_one(selector)
        if url_element and url_element.has_attr('href'):
            return url_element.get('href')
    
    # 가능한 모든 링크 확인
    for a_tag in item.find_all('a'):
        if a_tag.has_attr('href') and ('news.naver.com' in a_tag['href'] or 'n.news.naver.com' in a_tag['href']):
            return a_tag['href']
        
    # 일반 링크 확인
    for a_tag in item.find_all('a'):
        if a_tag.has_attr('href') and a_tag['href'].startswith('http'):
            return a_tag['href']
    
    return ""

def extract_source(item):
    """
    뉴스 아이템에서 출처(언론사)를 추출하는 함수
    """
    # 2025년 5월 최신 구조
    source_element = item.select_one('a.X0fMYp2dHd0TCUS2hjww.jTrMMxVViEpMe6SA4ef2 span.sds-comps-text-type-body2.sds-comps-text-weight-sm')
    if source_element:
        return source_element.get_text(strip=True)
        
    # 2025년 5월 구조
    source_element = item.select_one('div.sds-comps-profile-info-title span.sds-comps-text-type-body2.sds-comps-text-weight-sm')
    if source_element:
        return source_element.get_text(strip=True)

    # 더 간단한 선택자로 시도
    source_element = item.select_one('span.sds-comps-text-type-body2.sds-comps-text-weight-sm')
    if source_element:
        return source_element.get_text(strip=True)
    
    # 다른 가능한 선택자들
    selectors = [
        'a.info.press',
        'div.news_info a.info.press',
        'div.news_area div.news_info a.info.press',
        'div.news_dsc span.press',
        'div.news_info_group div.news_source',
        'div.news_contents span.news_source'
    ]
    
    for selector in selectors:
        source_element = item.select_one(selector)
        if source_element:
            return source_element.get_text(strip=True)
    
    return "Unknown"

def extract_date(item):
    """
    뉴스 아이템에서 날짜를 추출하는 함수
    """
    # 2025년 5월 최신 구조 - 예: "30분 전", "3일 전"
    date_elements = item.select('span.sds-comps-text-type-body2.sds-comps-text-weight-sm.sds-comps-profile-info-subtext')
    for date_elem in date_elements:
        # 처음 나오는 날짜와 관련된 텍스트 찾기
        if date_elem and ('전' in date_elem.text or '분' in date_elem.text or '일' in date_elem.text or '시간' in date_elem.text):
            return date_elem.get_text(strip=True)
    
    # 2025년 5월 구조
    date_element = item.select_one('span.sds-comps-text-type-body2.sds-comps-text-weight-sm.sds-comps-profile-info-subtext span.sds-comps-text-type-body2.sds-comps-text-weight-sm')
    if date_element:
        return date_element.get_text(strip=True)
    
    # 더 간단한 선택자
    date_element = item.select_one('span.sds-comps-profile-info-subtext span')
    if date_element:
        return date_element.get_text(strip=True)
    
    # 이전 버전 선택자들
    all_spans = item.select('span')
    for span in all_spans:
        text = span.get_text(strip=True)
        # 날짜/시간 패턴 확인 (예: "1시간 전", "5분 전", "어제", "2025.05.08." 등)
        if re.search(r'([0-9]+분|[0-9]+시간|일|주|달|년)( 전)?|어제|오늘|[0-9]{4}\.[0-9]{2}\.[0-9]{2}\.?', text):
            return text
    
    selectors = [
        'span.info',
        'div.news_info span.info',
        'div.news_area div.news_info span.info',
        'div.news_info_group div.news_time',
        'div.news_contents span.news_date'
    ]
    
    for selector in selectors:
        elements = item.select(selector)
        for element in elements:
            text = element.get_text(strip=True)
            if '전' in text or '분' in text or '시간' in text or '일' in text or '.' in text:
                return text
    
    return "Unknown"

def extract_content(item):
    """
    뉴스 아이템에서 내용(스니펫)을 추출하는 함수
    """
    # 2025년 5월 최신 구조
    content_element = item.select_one('a.X0fMYp2dHd0TCUS2hjww.IaKmSOGPdofdPwPE6cyU span.sds-comps-text-ellipsis-3.sds-comps-text-type-body1')
    if content_element:
        return content_element.get_text(strip=True)
    
    # 2025년 5월 구조
    content_element = item.select_one('a.X0fMYp2dHd0TCUS2hjww span.sds-comps-text-ellipsis-3.sds-comps-text-type-body1')
    if content_element:
        return content_element.get_text(strip=True)
    
    # 더 간단한 선택자로 시도
    content_element = item.select_one('span.sds-comps-text-ellipsis-3.sds-comps-text-type-body1')
    if content_element:
        return content_element.get_text(strip=True)
    
    # 다른 가능한 선택자들
    selectors = [
        'div.news_dsc',
        'a.api_txt_lines.dsc_txt_wrap',
        'div.news_area div.news_dsc',
        'div.news_wrap div.news_dsc',
        'div.news_contents p.news_description',
        'div.newslist_item p.newslist_item_desc'
    ]
    
    for selector in selectors:
        content_element = item.select_one(selector)
        if content_element:
            return content_element.get_text(strip=True)
    
    # 텍스트가 있는 p 태그 찾기
    for p_tag in item.find_all('p'):
        if p_tag.get_text(strip=True) and len(p_tag.get_text(strip=True)) > 20:
            return p_tag.get_text(strip=True)
    
    return ""

def extract_highlights(content_element):
    """
    내용에서 하이라이트(mark 태그)를 추출하는 함수
    """
    if not content_element:
        return []
    
    highlights = []
    
    # mark 태그로 하이라이트된 텍스트 찾기
    mark_tags = content_element.find_all('mark')
    if mark_tags:
        for mark in mark_tags:
            highlights.append(mark.get_text(strip=True))
        return highlights
    
    # mark 태그가 없으면 strong 태그 시도
    strong_tags = content_element.find_all('strong')
    if strong_tags:
        for strong in strong_tags:
            highlights.append(strong.get_text(strip=True))
        return highlights
    
    # strong 태그도 없으면 em 태그 시도
    em_tags = content_element.find_all('em')
    if em_tags:
        for em in em_tags:
            highlights.append(em.get_text(strip=True))
        return highlights
    
    # 다른 가능한 하이라이트 태그 시도
    highlight_tags = content_element.find_all(['b', 'span.highlight', 'span.emph'])
    if highlight_tags:
        for tag in highlight_tags:
            highlights.append(tag.get_text(strip=True))
    
    return highlights
