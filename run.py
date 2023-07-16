#%%
from tkinter import Tk, Label, Button, filedialog
from vibration_controller import VideoVibrationPlayer

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
arduino_port = int(os.getenv("ARDUINO_PORT"))
arduino_ip = os.getenv("ARDUINO_IP")

class VideoVibrationPlayerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Video Vibration Player")

        self.label = Label(master, text="Select video and subtitle files")
        self.label.pack()

        self.select_files_button = Button(master, text="Select Files", command=self.select_files)
        self.select_files_button.pack()

        self.start_button = Button(master, text="Start", command=self.start_player)
        self.start_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

        self.subtitle_file = None
        self.video_file = None

    def select_files(self):
        self.video_file = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
        self.subtitle_file = filedialog.askopenfilename(filetypes=[("Subtitle files", "*.srt")])

    def start_player(self):
        if self.video_file and self.subtitle_file:
            # Use the environment variables for the player configuration
            player = VideoVibrationPlayer(api_key=api_key, subtitle_file=self.subtitle_file, video_file=self.video_file, arduino_ip=arduino_ip, arduino_port=arduino_port)
            player.play()
        else:
            print("Please select video and subtitle files first")

root = Tk()
my_gui = VideoVibrationPlayerGUI(root)
root.mainloop()

# %%
