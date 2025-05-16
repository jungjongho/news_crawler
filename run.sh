#!/bin/bash

# 터미널 색상 설정
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== 네이버 뉴스 스크래퍼 웹 애플리케이션 시작 ===${NC}"

# 백엔드 실행
echo -e "${GREEN}백엔드 서버 시작 중...${NC}"
cd backend
if [ ! -d "venv" ]; then
    echo "가상환경 생성 중..."
    python -m venv venv
fi

# 가상환경 활성화
source venv/bin/activate || source venv/Scripts/activate

# 패키지 설치
echo "필요한 패키지 설치 중..."
pip install -r requirements.txt

# 백엔드 실행
echo "백엔드 서버 실행 중..."
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "백엔드 PID: $BACKEND_PID"

# 프론트엔드 실행
cd ../frontend
echo -e "${GREEN}프론트엔드 시작 중...${NC}"

# npm 패키지 설치
if [ ! -d "node_modules" ]; then
    echo "npm 패키지 설치 중..."
    npm install
fi

# 프론트엔드 실행
echo "프론트엔드 서버 실행 중..."
npm start &
FRONTEND_PID=$!
echo "프론트엔드 PID: $FRONTEND_PID"

echo -e "${YELLOW}서버가 실행되었습니다.${NC}"
echo -e "${GREEN}백엔드:${NC} http://localhost:8000"
echo -e "${GREEN}프론트엔드:${NC} http://localhost:3000"
echo "애플리케이션을 종료하려면 Ctrl+C를 누르세요."

# 종료 시 프로세스 정리
function cleanup {
    echo -e "\n${YELLOW}서버 종료 중...${NC}"
    kill $BACKEND_PID
    kill $FRONTEND_PID
    echo -e "${GREEN}서버가 종료되었습니다.${NC}"
    exit 0
}

trap cleanup SIGINT

# 무한 대기
while true; do
    sleep 1
done
