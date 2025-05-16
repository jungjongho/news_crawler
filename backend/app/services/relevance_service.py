#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import pandas as pd
import os
import requests
import json
import logging
import re
from typing import Dict, Any, Optional, Tuple, List
import traceback

from app.utils.csv_utils import read_csv, save_to_csv, get_csv_statistics
from app.core.config import settings

logger = logging.getLogger(__name__)

class RelevanceService:
    """
    뉴스 관련성 평가 서비스
    """
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        서비스 초기화
        
        Args:
            api_key: OpenAI API 키
            model: 사용할 LLM 모델 (기본값: gpt-3.5-turbo)
        """
        self.api_key = api_key
        self.model = model
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # OpenAI API 엔드포인트
        self.api_url = "https://api.openai.com/v1/chat/completions"
        
        # Claude API 사용 시 URL 변경 필요
        # self.api_url = "https://api.anthropic.com/v1/messages"
        # self.headers = {
        #     "Content-Type": "application/json",
        #     "anthropic-version": "2023-06-01",
        #     "x-api-key": api_key
        # }
    
    def check_article_relevance(self, article: Dict[str, Any]) -> Tuple[bool, str, str]:
        """
        기사의 적합성 판단 및 카테고리 분류
        
        Args:
            article: 평가할 기사 정보
            
        Returns:
            (적합성 여부, 적합성 이유, 카테고리)
        """
        title = article.get('title', "")
        source = article.get('source', "")
        date = article.get('date', "")
        content = article.get('content', "")
        keyword = article.get('keyword', "")
        
        prompt = f"""
        당신은 화장품 업계 정보 분석가입니다. 아래의 기사를 분석하여 적합성과 카테고리를 판단해주세요.
        
        제목: {title}
        출처: {source} 
        날짜: {date}
        내용: {content}
        검색 키워드: {keyword}
        
        ### 첫 번째 태스크: 적합성 판단 ###
        이 기사가 화장품 연구원이나 화장품 ODM 기업 임직원에게 전달해도 될만한 가치가 있는지 평가해주세요.
        
        중요: 제목과 내용을 모두 면밀히 검토하여 다음 기준에 따라 판단해주세요.
        
        1. 화장품 업계 트렌드나 시장 현황을 제공하는지
        2. 화장품 원료나 기술에 관한 정보를 담고 있는지
        3. 경쟁사나 산업 내 중요한 변화를 담고 있는지
        4. 규제나 법적 변경사항에 대한 정보를 포함하는지
        5. 화장품 연구 개발이나 제조에 영향을 줄 수 있는 내용인지
        6. 화장품 ODM 기업 활동이나 전략에 대한 정보를 담고 있는지
        7. 화장품 산업 내 협업이나 인수합병 정보를 포함하는지
        8. 화장품 회사들의 실적이나 주가 정보를 담고 있는지
        9. 유의미한 국제 무역이나 관세 정책 정보를 담고 있는지
        
        위 항목 중 하나라도 해당된다면 가치가 있다고 판단하고 True로, 그렇지 않다면 False로 응답해주세요.
        
        ### 두 번째 태스크: 카테고리 분류 ###
        기사의 내용을 기반으로 다음 4가지 카테고리 중 하나로 분류해주세요:
        
        1. 자사 언급기사: 코스맥스(회사명 "코스맥스", "Cosmax", "코스맥스비티아이" 등)가 직접 언급된 기사
        2. 업계 관련기사: 코스맥스 외 화장품 회사(특히 화장품 제조회사)에 관한 기사 (예: 한국콜마, 아모레퍼시픽, LG생활건강, 코스메카코리아 등)
        3. 건강기능식품·펫푸드: 건강기능식품, 영양제, 펫푸드, 마이크로바이옴, 식품의약품안전처 관련 기사
        4. 기타: 위 세 카테고리에 해당하지 않는 기사 (예: K유통, 일반 소비재 등)
        
        기사가 여러 카테고리에 해당할 경우, 더 높은 우선순위의 카테고리를 선택하세요 (우선순위: 자사 언급기사 > 업계 관련기사 > 건강기능식품·펫푸드 > 기타).
        
        응답 형식:
        적합성: [true/false]
        이유: [간략한 이유 설명]
        카테고리: [자사 언급기사/업계 관련기사/건강기능식품·펫푸드/기타]
        
        위 형식에 맞게 답변해주세요.
        """
        
        try:
            # OpenAI API 호출
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 300
            }
            
            # Claude API 사용 시 페이로드 변경 필요
            # payload = {
            #     "model": "claude-3-haiku-20240307",
            #     "max_tokens": 300,
            #     "temperature": 0.3,
            #     "system": "You are a cosmetic industry analyst who evaluates news relevance and categorizes them accurately.",
            #     "messages": [{"role": "user", "content": prompt}]
            # }
            
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                response_data = response.json()
                
                # OpenAI 응답 처리
                result_text = response_data["choices"][0]["message"]["content"]
                
                # Claude 응답 처리시 변경 필요
                # result_text = response_data["content"][0]["text"]
                
                # 정규 표현식으로 응답에서 필요한 정보 추출
                is_relevant_match = re.search(r'적합성:\s*(true|false)', result_text, re.IGNORECASE)
                reason_match = re.search(r'이유:\s*(.+?)(?=\n|$)', result_text)
                category_match = re.search(r'카테고리:\s*(자사 언급기사|업계 관련기사|건강기능식품·펫푸드|기타)', result_text)
                
                # 적합성 추출
                if is_relevant_match:
                    is_relevant = is_relevant_match.group(1).lower() == 'true'
                else:
                    # 적합성 정보가 없으면 텍스트에서 추론
                    is_relevant = 'true' in result_text.lower() and not ('false' in result_text.lower() and 'true' not in result_text.lower())
                
                # 이유 추출
                if reason_match:
                    reason = reason_match.group(1).strip()
                else:
                    # 이유가 없으면 기본 이유 설정
                    reason = "이유가 명확히 제시되지 않음"
                
                # 카테고리 추출
                if category_match:
                    category = category_match.group(1)
                else:
                    # 카테고리 정보가 없으면 텍스트에서 추론
                    if "자사" in result_text.lower() or "코스맥스" in result_text.lower():
                        category = "자사 언급기사"
                    elif "업계" in result_text.lower() or "화장품" in result_text.lower():
                        category = "업계 관련기사"
                    elif "건강" in result_text.lower() or "펫" in result_text.lower() or "식품" in result_text.lower():
                        category = "건강기능식품·펫푸드"
                    else:
                        category = "기타"
                
                return is_relevant, reason, category
            else:
                logger.error(f"API 오류: {response.status_code}, {response.text}")
                return False, f"API 오류: {response.status_code}", "기타"
        
        except Exception as e:
            logger.error(f"오류 발생: {str(e)}")
            traceback.print_exc()
            return False, f"요청 처리 중 오류: {str(e)}", "기타"
    
    def process_file(self, file_path: str) -> Tuple[Optional[str], Dict[str, Any]]:
        """
        CSV 파일 처리 및 적합성 판단 결과 추가
        
        Args:
            file_path: 처리할 CSV 파일 경로
            
        Returns:
            (저장된 파일 경로, 통계 정보)
        """
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None, {"error": "File not found"}
        
        try:
            logger.info(f"Loading file: {file_path}")
            # CSV 파일 읽기
            data = read_csv(file_path, encoding='utf-8-sig')
            
            # 이미 'is_relevant' 열이 있는지 확인
            if data and 'is_relevant' in data[0] and 'category' in data[0]:
                logger.info(f"File '{file_path}' already processed")
                
                # 파일 통계 가져오기
                stats = get_csv_statistics(file_path)
                stats["already_processed"] = True
                
                return file_path, stats
            
            # 각 기사 처리
            processed_data = []
            for idx, row in enumerate(data):
                # 진행 로그
                if idx % 10 == 0:
                    logger.info(f"Processing article {idx+1}/{len(data)}")
                
                # 적합성 판단 및 카테고리 분류
                is_relevant, reason, category = self.check_article_relevance(row)
                
                # 결과 업데이트
                row['is_relevant'] = is_relevant
                row['relevance_reason'] = reason
                row['category'] = category
                
                processed_data.append(row)
            
            # 결과 저장
            base_name = os.path.basename(file_path)
            output_file = os.path.join(os.path.dirname(file_path), base_name.replace('.csv', '_evaluated.csv'))
            
            success = save_to_csv(processed_data, output_file, encoding='utf-8-sig')
            if not success:
                logger.error(f"Failed to save evaluated results to {output_file}")
                return None, {"error": "Failed to save evaluated results"}
            
            logger.info(f"Saved evaluated results to {output_file}")
            
            # 통계 정보 계산
            stats = get_csv_statistics(output_file)
            
            return output_file, stats
            
        except Exception as e:
            logger.error(f"Error processing file '{file_path}': {str(e)}")
            traceback.print_exc()
            return None, {"error": str(e)}
