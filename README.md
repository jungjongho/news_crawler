# 네이버 뉴스 스크래퍼 웹 애플리케이션

키워드 기반으로 네이버 뉴스를 수집하고 관련성을 평가하는 웹 애플리케이션입니다.

## 주요 기능

1. **뉴스 수집**: 원하는 키워드로 네이버 뉴스를 검색하고 수집합니다.
2. **관련성 평가**: OpenAI API를 사용하여 화장품 업계 관련성을 평가합니다.
3. **결과 분석**: 카테고리 분류, 통계, 차트 등을 통해 결과를 시각화합니다.
4. **파일 관리**: 수집/평가 결과를 CSV 파일로 저장하고 다운로드할 수 있습니다.

## 기술 스택

### 백엔드
- **프레임워크**: FastAPI
- **크롤링**: Requests, BeautifulSoup4
- **데이터 처리**: Pandas
- **AI 통합**: OpenAI API
- **기타**: Python 3.8+

### 프론트엔드
- **프레임워크**: React, React Router
- **UI 라이브러리**: Material-UI (MUI)
- **차트**: Chart.js, react-chartjs-2
- **HTTP 클라이언트**: Axios
- **기타**: JavaScript (ES6+)

## 설치 및 실행 방법

### 요구사항
- Python 3.8+
- Node.js 14+
- npm 6+

### 설치

1. 저장소 클론
   ```bash
   git clone https://github.com/your-username/news_crawler.git
   cd news_crawler
   ```

2. 백엔드 설정
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. 프론트엔드 설정
   ```bash
   cd ../frontend
   npm install
   ```

### 실행

#### 한 번에 실행 (쉘 스크립트)
```bash
chmod +x run.sh  # 실행 권한 부여
./run.sh  # 스크립트 실행
```

#### 수동으로 실행

1. 백엔드 실행
   ```bash
   cd backend
   source venv/bin/activate  # Windows: venv\Scripts\activate
   python run.py
   ```

2. 프론트엔드 실행
   ```bash
   cd ../frontend
   npm start
   ```

### 접속 방법
- 백엔드: http://localhost:8000
- 프론트엔드: http://localhost:3000

## 사용 방법

1. **뉴스 수집**
   - 홈페이지에서 '뉴스 수집' 메뉴 선택
   - 검색 키워드 입력 또는 추천 키워드 카테고리 선택
   - 키워드당 최대 뉴스 수 설정
   - '뉴스 수집 시작' 버튼 클릭

2. **관련성 평가**
   - '관련성 평가' 메뉴 선택
   - 평가할 파일 선택
   - OpenAI API 키 입력 및 모델 선택
   - '관련성 평가 시작' 버튼 클릭

3. **결과 확인**
   - '결과 목록' 메뉴 선택
   - 파일 목록에서 확인할 파일 선택
   - 카테고리 분석, 관련성 분석, 키워드 분석 탭에서 결과 확인
   - 파일 다운로드 또는 미리보기 가능

## 주의사항

- OpenAI API 키는 사용자의 브라우저에 저장되며, 서버로 전송되지는 않습니다.
- 네이버 뉴스 웹 구조 변경 시 크롤링이 정상적으로 작동하지 않을 수 있습니다. (2025년 5월 기준 업데이트 완료)
- HTML 선택자: `#main_pack > section.sc_new.sp_nnews._fe_news_collection._prs_nws > div.api_subject_bx > div.group_news > ul > li`
- 업데이트된 선택자: `ul.list_news._infinite_list li` 혹은 `div.sds-comps-vertical-layout.sds-comps-full-layout.iYo99IP8GixD0iM_4cb8`
- 과도한 크롤링은 네이버의 차단을 받을 수 있으니 적절히 사용해주세요.

## 라이선스

MIT License

## 개발자 정보

- 이름: Your Name
- 이메일: your.email@example.com
