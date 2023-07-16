#%%
import vlc
import socket
import time
from str_convert import SceneAnalyzer

class VideoVibrationPlayer:
    def __init__(self, api_key, subtitle_file, video_file, arduino_ip, arduino_port):
        self.api_key = api_key
        self.subtitle_file = subtitle_file
        self.video_file = video_file
        self.arduino_ip = arduino_ip
        self.arduino_port = arduino_port
        self.analyzer = SceneAnalyzer(api_key, subtitle_file)

    def convert_time_to_seconds(self, time_string):
        hours, minutes, seconds_ms = time_string.split(':')
        seconds, milliseconds = seconds_ms.split(',')
        return 3600 * int(hours) + 60 * int(minutes) + int(seconds)

    def extract_event_values(self, event):
        time_range, intensity = event
        start_time_string, end_time_string = time_range.split(' --> ')
        start_time = self.convert_time_to_seconds(start_time_string)
        end_time = self.convert_time_to_seconds(end_time_string)
        return start_time, end_time, intensity

    def send_intensity(self, connection, intensity):
        connection.send(str(intensity).encode())

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
    player.play()