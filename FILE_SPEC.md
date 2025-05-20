네이버 뉴스 스크래퍼 파일 및 기능 명세서
프로젝트 개요
네이버 뉴스 스크래퍼는 키워드 기반으로 네이버 뉴스를 수집하고 관련성을 평가하는 웹 애플리케이션입니다. 주요 기능으로는 뉴스 수집, 관련성 평가, 결과 분석 및 파일 관리가 있습니다.
디렉토리 구조 개요
/news_crawler
├── README.md
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── requirements.txt
│   ├── results/
│   └── run.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   └── utils/
│   ├── package.json
│   └── package-lock.json
├── run.bat
└── run.sh
백엔드 파일 상세
메인 파일

/backend/run.py

기능: 백엔드 애플리케이션 시작점
주요 기능:

FastAPI 애플리케이션 실행
명령행 인자 처리(호스트, 포트, 재로드 등)
로깅 설정
결과 디렉토리 생성 확인




/backend/app/main.py

기능: FastAPI 애플리케이션 설정
주요 기능:

FastAPI 인스턴스 생성 및 설정
CORS 미들웨어 설정
API 라우터 등록
로깅 설정
정적 파일 서빙 설정





API 엔드포인트

/backend/app/api/endpoints/crawler.py

기능: 뉴스 크롤링 관련 API 엔드포인트
주요 엔드포인트:

/api/crawler/crawl: 키워드 기반 뉴스 크롤링
/api/crawler/files: 크롤링 결과 파일 목록 조회
/api/crawler/files/{file_name}/preview: 파일 내용 미리보기
/api/crawler/files/{file_name}/statistics: 파일 통계 정보
/api/crawler/files/{file_name}/download-link: 파일 다운로드 링크 생성




/backend/app/api/endpoints/relevance.py

기능: 뉴스 관련성 평가 API 엔드포인트
주요 엔드포인트:

/api/relevance/evaluate: 뉴스 기사의 관련성 평가


기능 설명: OpenAI API를 활용해 뉴스의 화장품 업계 관련성을 평가하고 카테고리 분류


/backend/app/api/endpoints/download.py

기능: 파일 다운로드 관련 API 엔드포인트
주요 엔드포인트:

/api/download/{file_name}: 파일 다운로드
/api/download/zip/{folder_name}: 폴더 압축 다운로드





서비스 레이어

/backend/app/services/crawler_service.py

기능: 뉴스 크롤링 서비스
주요 기능:

네이버 뉴스 검색 URL 생성
HTML 파싱 및 뉴스 아이템 추출
키워드 기반 뉴스 수집
결과 CSV 파일 저장




/backend/app/services/relevance_service.py

기능: 뉴스 관련성 평가 서비스
주요 기능:

OpenAI API 연동
뉴스 기사 적합성 판단 및 카테고리 분류
CSV 파일 처리 및 평가 결과 추가




/backend/app/services/mail_service.py

기능: 이메일 발송 서비스
주요 기능:

SMTP 서버 연동
이메일 작성 및 발송
파일 첨부 지원





유틸리티 및 기타

/backend/app/utils/

naver_news_helper.py: 네이버 뉴스 파싱 헬퍼 함수
csv_utils.py: CSV 파일 처리 유틸리티


/backend/app/core/

config.py: 애플리케이션 설정 (환경 변수, 경로 등)


/backend/app/models/

schemas.py: Pydantic 모델 스키마 정의



프론트엔드 파일 상세
API 클라이언트

/frontend/src/api/client.js

기능: API 클라이언트 설정
주요 기능:

Axios 인스턴스 생성 및 설정
요청/응답 인터셉터 설정
에러 처리




/frontend/src/api/crawlerService.js

기능: 크롤러 API 서비스
주요 기능:

뉴스 크롤링 요청
파일 목록 조회
파일 미리보기 및 통계 조회




/frontend/src/api/relevanceService.js

기능: 관련성 평가 API 서비스
주요 기능:

OpenAI API 키를 사용한 관련성 평가 요청




/frontend/src/api/downloadService.js

기능: 파일 다운로드 서비스
주요 기능:

다운로드 링크 생성
파일 직접 다운로드
압축 파일 다운로드





페이지 컴포넌트

/frontend/src/pages/HomePage.js

기능: 홈페이지/랜딩 페이지
설명: 애플리케이션 소개 및 주요 기능 링크 제공


/frontend/src/pages/CrawlerPage.js

기능: 뉴스 수집 페이지
주요 기능:

키워드 입력 및 관리
추천 키워드 카테고리 선택
크롤링 설정 (최대 뉴스 수 등)
크롤링 실행 및 결과 표시




/frontend/src/pages/RelevancePage.js

기능: 관련성 평가 페이지
주요 기능:

평가할 파일 선택
OpenAI API 키 입력 및 관리
AI 모델 선택
관련성 평가 실행 및 결과 표시




/frontend/src/pages/ResultsPage.js

기능: 결과 분석 페이지
주요 기능:

크롤링/평가 결과 파일 목록 표시
파일 내용 미리보기
통계 및 차트 표시
카테고리별 분석




/frontend/src/pages/NotFoundPage.js

기능: 404 에러 페이지



유틸리티 및 기타

/frontend/src/utils/helpers.js

기능: 유틸리티 함수 모음
주요 기능:

로컬 스토리지 관리
배열 중복 제거
날짜/시간 포맷팅 등




/frontend/src/components/common/

PageTitle.js: 페이지 제목 컴포넌트
AlertMessage.js: 알림 메시지 컴포넌트
LoadingOverlay.js: 로딩 오버레이 컴포넌트



기능별 흐름 설명
1. 뉴스 수집 흐름

사용자가 프론트엔드에서 키워드 입력 및 설정 구성
frontend/src/api/crawlerService.js의 crawlNews 함수 호출
백엔드 app/api/endpoints/crawler.py의 /api/crawler/crawl 엔드포인트 처리
app/services/crawler_service.py의 crawl_keywords 함수 실행
각 키워드별로 네이버 뉴스 크롤링 (crawl_keyword 함수)
결과를 CSV 파일로 저장 (save_results 함수)
프론트엔드로 결과 반환 및 표시

2. 관련성 평가 흐름

사용자가 파일 선택 및 OpenAI API 키 입력
frontend/src/api/relevanceService.js의 evaluateNews 함수 호출
백엔드 app/api/endpoints/relevance.py의 /api/relevance/evaluate 엔드포인트 처리
app/services/relevance_service.py의 process_file 함수 실행
각 뉴스 기사에 대해 check_article_relevance 함수 호출
OpenAI API를 통해 관련성 평가 및 카테고리 분류
결과를 CSV 파일에 추가하여 저장
프론트엔드로 결과 반환 및 표시

3. 결과 다운로드 흐름

사용자가 파일 다운로드 요청
frontend/src/api/downloadService.js의 downloadFile 함수 호출
백엔드 app/api/endpoints/download.py의 /api/download/{file_name} 엔드포인트 처리
FileResponse를 통해 파일 다운로드 스트림 생성
사용자 브라우저에 파일 다운로드

중요 환경 변수 및 설정

/backend/app/core/config.py에서 관리되는 주요 설정:

RESULTS_PATH: 결과 파일 저장 경로
AUTO_COPY_TO_DOWNLOADS: 결과 파일 다운로드 폴더에 자동 복사 여부
USER_DOWNLOAD_PATH: 사용자 다운로드 폴더 경로



네이버 뉴스 크롤링 CSS 선택자

기본 선택자: ul.list_news._infinite_list li
대체 선택자: div.sds-comps-vertical-layout.sds-comps-full-layout.iYo99IP8GixD0iM_4cb8
XPath: //*[@id="main_pack"]/section[1]/div[1]/div[2]/ul

사용 기술

백엔드: FastAPI, Python, BeautifulSoup, OpenAI API
프론트엔드: React, Material-UI, Axios, Chart.js
데이터 저장: CSV 파일 형식

주의사항

OpenAI API 키는 프론트엔드 로컬 스토리지에 저장되며, 서버로 전송됩니다 (평가 요청 시)
네이버 웹 구조 변경 시 크롤링 로직 업데이트 필요
과도한 크롤링은 네이버의 차단을 받을 수 있음