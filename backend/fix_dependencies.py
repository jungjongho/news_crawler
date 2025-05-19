#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
패키지 호환성 문제 해결을 위한 스크립트
"""

import subprocess
import sys
import os

def main():
    """
    패키지 버전 충돌을 해결하기 위한 스크립트
    """
    print("패키지 호환성 문제 해결 중...")
    
    # 현재 설치된 urllib3 버전 확인
    try:
        import urllib3
        print(f"현재 urllib3 버전: {urllib3.__version__}")
    except ImportError:
        print("urllib3가 설치되어 있지 않습니다.")
    
    # 특정 버전의 urllib3 설치 (OpenSSL 관련 경고 해결)
    print("urllib3 1.26.18 버전 설치 중...")
    subprocess.call([sys.executable, "-m", "pip", "install", "urllib3==1.26.18"])
    
    print("패키지 버전 호환성 문제 해결 완료!")
    print("이제 'python run.py'를 다시 실행하세요.")

if __name__ == "__main__":
    main()
