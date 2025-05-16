@echo off
echo === 네이버 뉴스 스크래퍼 웹 애플리케이션 시작 ===

REM 백엔드 실행
echo 백엔드 서버 시작 중...
cd backend

if not exist "venv" (
    echo 가상환경 생성 중...
    python -m venv venv
)

REM 가상환경 활성화
call venv\Scripts\activate

REM 패키지 설치
echo 필요한 패키지 설치 중...
pip install -r requirements.txt

REM 백엔드 실행
echo 백엔드 서버 실행 중...
start python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

REM 프론트엔드 실행
cd ..\frontend
echo 프론트엔드 시작 중...

REM npm 패키지 설치
if not exist "node_modules" (
    echo npm 패키지 설치 중...
    call npm install
)

REM 프론트엔드 실행
echo 프론트엔드 서버 실행 중...
start npm start

echo 서버가 실행되었습니다.
echo 백엔드: http://localhost:8000
echo 프론트엔드: http://localhost:3000
echo 애플리케이션을 종료하려면 각 터미널 창을 닫으세요.

pause
