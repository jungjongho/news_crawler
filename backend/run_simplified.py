#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uvicorn
import argparse
import os
import logging

if __name__ == "__main__":
    # 명령행 인자 처리
    parser = argparse.ArgumentParser(description='네이버 뉴스 스크래퍼 API 서버')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='서버 호스트 (기본값: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000, help='서버 포트 (기본값: 8000)')
    parser.add_argument('--reload', action='store_true', help='자동 재로드 활성화')
    parser.add_argument('--debug', action='store_true', help='디버그 로그 활성화')
    args = parser.parse_args()
    
    # 로깅 설정
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # 결과 디렉토리 확인 및 생성
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    print("=" * 80)
    print("네이버 뉴스 스크래퍼 API 서버 시작 (간소화 버전)")
    print("이 버전은 pandas와 numpy 의존성이 제거된 버전입니다.")
    print("=" * 80)
    
    # Uvicorn 서버 실행
    uvicorn.run(
        "app.main:app", 
        host=args.host, 
        port=args.port,
        reload=args.reload,
        log_level="debug" if args.debug else "info"
    )
