#%%
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from vibration_controller import VideoVibrationPlayer
from dotenv import load_dotenv
import os

# 환경 변수를 불러오는 부분
load_dotenv()

# 필요한 환경 변수를 설정하는 부분
api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play_video', methods=['POST'])
def play_video():
    subtitle_file = request.form.get('subtitle_file')
    video_file = request.form.get('video_file')

    player = VideoVibrationPlayer(api_key=api_key, subtitle_file=subtitle_file, video_file=video_file)
    player.play()

    return "Video started"

@socketio.on('vibration')
def handle_vibration(data):
    print('Received vibration:', data)
    socketio.emit('vibrate', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='192.168.0.9', port=5000)

