# Video Vibration Player

이 프로젝트는 영상의 자막 내용을 분석하여 해당 씬의 강도를 판단하고, 이를 통해 연결된 진동 기기를 제어하는 어플리케이션입니다. 프로젝트는 아래의 부분으로 나뉩니다.

## 구성 요소

- **영상 자막 분석**: GPT-4 모델을 사용하여 각 자막의 내용을 분석하고 씬의 강도를 0에서 10 사이의 숫자로 평가합니다.
- **진동 기기 제어**: 분석된 결과를 사용하여 진동 기기를 제어합니다. 진동 기기는 WiFi를 통해 연결됩니다.
- **GUI**: 사용자가 비디오 파일과 자막 파일을 선택하고 플레이어를 시작할 수 있게 하는 GUI입니다.

이 프로젝트는 다음의 파이썬 스크립트 및 아두이노 스케치로 구성되어 있습니다.

### Python 스크립트

- `str_convert.py`: 이 스크립트는 주어진 자막 파일을 처리하고 각 자막의 내용을 GPT-4 모델에 제출하여 씬의 강도를 평가하는 SceneAnalyzer 클래스를 정의합니다.
- `vibration_controller.py`: 이 스크립트는 VideoVibrationPlayer 클래스를 정의하며, 이 클래스는 비디오를 재생하고 SceneAnalyzer를 사용하여 각 씬의 진동 강도를 결정한 후 해당 강도를 아두이노에 전송하여 진동 모터를 제어합니다.
- `run.py`: 이 스크립트는 VideoVibrationPlayerGUI 클래스를 정의하며, 이 클래스는 사용자가 비디오 파일과 자막 파일을 선택하고 VideoVibrationPlayer를 시작할 수 있는 간단한 GUI를 제공합니다.

### 아두이노 스케치

- `index.ino`: 이 스케치는 WiFi를 통해 연결된 클라이언트로부터 수신한 메시지를 기반으로 진동 모터를 제어합니다.

## 설치 및 사용 방법

1. `str_convert.py`, `vibration_controller.py`, `run.py` 스크립트를 다운로드하고 파이썬 환경에 설치합니다.
2. 아두이노 IDE를 사용하여 `index.ino`를 아두이노에 업로드합니다.
3. `run.py`를 실행하여 GUI를 시작합니다.
4. "Select Files" 버튼을 클릭하여 비디오 파일과 자막 파일을 선택합니다.
5. "Start" 버튼을 클릭하여 VideoVibrationPlayer를 시작합니다.
6. 영상이 재생되면서, 각 씬에 해당하는 진동이 생성됩니다.

## 의존성

이 프로젝트는 다음의 라이브러리에 의존합니다:

### Python:

- openai
- vlc
- python-vlc
- python-dotenv
- tkinter

### Arduino:

- WiFiS3
- Wire
- LiquidCrystal_I2C

이 프로젝트를 위한 모든 파이썬 라이브러리 의존성은 `requirements.txt` 파일에 나열되어 있습니다. 이를 사용하여 필요한 라이브러리를 쉽게 설치할 수 있습니다.

```
pip install -r requirements.txt
```

본 프로젝트는 Python 3.10.0 버전에서 테스트 및 개발되었습니다. 

## 주의 사항

이 프로젝트를 사용하기 위해서는 OpenAI의 GPT-4 모델에 접근할 수 있는 API 키가 필요합니다. 또한 아두이노를 WiFi에 연결하기 위한 SSID와 비밀번호가 필요합니다.

## 기타

이 프로젝트는 동의대학교 2023년도 하계 계절학기 융복합캡스톤디자인의 프로젝트 결과물 입니다.
