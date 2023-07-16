#%%
from tkinter import Tk, Label, Button, filedialog
from vibration_controller import VideoVibrationPlayer

from dotenv import load_dotenv
import os

# 환경 변수를 불러오는 부분
load_dotenv()

# 필요한 환경 변수를 설정하는 부분
api_key = os.getenv("OPENAI_API_KEY")
arduino_port = int(os.getenv("ARDUINO_PORT"))
arduino_ip = os.getenv("ARDUINO_IP")

class VideoVibrationPlayerGUI:
    def __init__(self, master):
        self.master = master # Tk 객체
        master.title("Video Vibration Player") # GUI 창 제목 설정

        # 간단한 레이블을 생성하여 GUI에 추가
        self.label = Label(master, text="Select video and subtitle files")
        self.label.pack()

        # 파일 선택 버튼을 생성하고, 버튼 클릭 시 self.select_files 메소드가 호출되도록 설정        
        self.select_files_button = Button(master, text="Select Files", command=self.select_files)
        self.select_files_button.pack()

        # 재생 버튼을 생성하고, 버튼 클릭 시 self.start_player 메소드가 호출되도록 설정
        self.start_button = Button(master, text="Start", command=self.start_player)
        self.start_button.pack()

        # 프로그램 종료 버튼 생성      
        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

        # 자막 파일과 비디오 파일의 경로를 저장할 변수 초기화       
        self.subtitle_file = None
        self.video_file = None

    # 파일 선택 다이얼로그를 통해 비디오 파일과 자막 파일을 선택하는 메소드    
    def select_files(self):
        self.video_file = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
        self.subtitle_file = filedialog.askopenfilename(filetypes=[("Subtitle files", "*.srt")])

    # 선택한 비디오 파일과 자막 파일로 VideoVibrationPlayer를 시작하는 메소드
    def start_player(self):
        if self.video_file and self.subtitle_file:
            # Use the environment variables for the player configuration
            player = VideoVibrationPlayer(api_key=api_key, subtitle_file=self.subtitle_file, video_file=self.video_file, arduino_ip=arduino_ip, arduino_port=arduino_port)
            player.play()
        else:
            print("Please select video and subtitle files first")

root = Tk() # Tk 객체 생성
my_gui = VideoVibrationPlayerGUI(root) # GUI 인스턴스 생성
root.mainloop() # GUI 시작

# %%
