#%%
import vlc
import socket
import time
from str_convert import SceneAnalyzer

class VideoVibrationPlayer:
    def __init__(self, api_key, subtitle_file, video_file, arduino_ip, arduino_port):
        self.api_key = api_key # OpenAI GPT-4를 사용하기 위한 API 키
        self.subtitle_file = subtitle_file # 분석할 자막 파일의 경로
        self.video_file = video_file # 재생할 비디오 파일의 경로
        self.arduino_ip = arduino_ip # 아두이노 서버의 IP 주소
        self.arduino_port = arduino_port # 아두이노 서버의 포트 번호
        self.analyzer = SceneAnalyzer(api_key, subtitle_file)  # 장면 분석 객체 생성
        
    # 시간 문자열을 초 단위로 변환하는 메소드
    def convert_time_to_seconds(self, time_string):
        hours, minutes, seconds_ms = time_string.split(':')
        seconds, milliseconds = seconds_ms.split(',')
        return 3600 * int(hours) + 60 * int(minutes) + int(seconds)
        
    # 이벤트 데이터를 추출하는 메소드
    def extract_event_values(self, event):
        time_range, intensity = event
        start_time_string, end_time_string = time_range.split(' --> ')
        start_time = self.convert_time_to_seconds(start_time_string)
        end_time = self.convert_time_to_seconds(end_time_string)
        return start_time, end_time, intensity
    # 아두이노 서버에 강도 값을 전송하는 메소드
    def send_intensity(self, connection, intensity):
        connection.send(str(intensity).encode())

    # 비디오와 진동을 동기화하여 재생하는 메소드
    def play(self):
        events = self.analyzer.process_subtitle()

        connection = socket.socket()
        connection.connect((self.arduino_ip, self.arduino_port))

        player = vlc.MediaPlayer(self.video_file)
        player.play()

        last_end_time = 0
        for event in events:
            start_time, end_time, intensity = self.extract_event_values(event)
            
            time.sleep(start_time - last_end_time)
            self.send_intensity(connection, intensity)
            
            time.sleep(end_time - start_time)
            self.send_intensity(connection, 0)
            
            last_end_time = end_time

        connection.close()


if __name__ == '__main__':
    player = VideoVibrationPlayer(api_key='your_key', subtitle_file='your_subtitle.srt', video_file='your_video.mp4', arduino_ip='your_arduino_ip', arduino_port='')
    player.play() # 비디오 재생
