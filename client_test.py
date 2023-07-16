#%%
import socket

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

arduino_port = int(os.getenv("ARDUINO_PORT"))
arduino_ip = os.getenv("ARDUINO_IP")

# 소캣 객체를 생성합니다.
s = socket.socket()

# 연결할 포트 정의
port = arduino_port  # Arduino port

# 로컬 서버 연결
s.connect((arduino_ip, port))

# 데이터 전송
s.send(b'0')

# 연결 종료
s.close()