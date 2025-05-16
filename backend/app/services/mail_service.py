#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class MailService:
    """
    메일 발송 서비스
    """
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        """
        서비스 초기화
        
        Args:
            smtp_server: SMTP 서버 주소
            smtp_port: SMTP 서버 포트
            username: SMTP 사용자 이름 (보통 이메일 주소)
            password: SMTP 비밀번호
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
    
    def send_mail(self, 
                  recipients: List[str], 
                  subject: str, 
                  body: str, 
                  file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        이메일 발송
        
        Args:
            recipients: 수신자 이메일 주소 목록
            subject: 이메일 제목
            body: 이메일 본문
            file_path: 첨부 파일 경로 (선택 사항)
            
        Returns:
            결과 정보
        """
        try:
            # 이메일 생성
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = ", ".join(recipients)
            msg['Subject'] = subject
            
            # 본문 추가
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # 파일 첨부 (있는 경우)
            if file_path and os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    part = MIMEApplication(file.read(), Name=os.path.basename(file_path))
                
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                msg.attach(part)
                logger.info(f"Attached file: {file_path}")
            elif file_path:
                logger.warning(f"File not found: {file_path}")
            
            # SMTP 서버 연결 및 메일 발송
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # TLS 보안 연결
                server.login(self.username, self.password)
                server.send_message(msg)
                logger.info(f"Email sent to {len(recipients)} recipients")
            
            return {
                "success": True,
                "message": f"Email sent to {len(recipients)} recipients",
                "recipients": recipients
            }
            
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to send email: {str(e)}",
                "error": str(e)
            }
