# Speech-Recognition-System

*COMPANY*: CODTECH IT SOLUTIONS

*NAME*: MD JAWAD

*INTERN ID*: CT04DR1325

*DOMAIN*: ARTIFICIAL INTELLIGENCE

*DURATION*: 4 WEEKS

*MENTOR*: NEELA SANTOSH KUMAR

DESCRIPTION:

🗣️ Speech Recognition App — Python | Google API | Wav2Vec2 | Real-Time STT

A powerful and extensible Speech-to-Text (STT) application built using Python.
The system supports multiple speech engines, real-time microphone recording, offline/online transcription, audio processing, and a simple GUI interface.

This project was created as part of my Artificial Intelligence Internship, and showcases my ability to integrate audio signal processing, transformer-based AI models, Python automation, and GUI development.

⭐ Features
🔊 Multi-Engine Speech Recognition

Google Web Speech API (online)

Wav2Vec2 Transformer Model (offline)

(Sphinx available but disabled due to Windows build issues)

🎤 Real-Time Microphone Recording

Automatically detects available microphones

Streams audio input using PyAudio

Supports noise-reduced recording

🧠 Transformer-based AI Model (Wav2Vec2)

Supports CPU/GPU inference

Automatic selection of device

Offline speech recognition using HuggingFace models

🛠️ Utilities & Tools Included

Logging system

Timestamp formatting

Transcription file saving

Complete unit test suite (test_system.py)

🪟 Simple GUI Interface

Start/Stop recording

Engine selection

Microphone selection

Live transcription display

Save transcription as .txt

📁 Project Structure
speechRecognitionApp/
│── gui_app.py              # Main GUI application
│── audio_handler.py        # Microphone and audio utilities
│── speech_recognizer.py    # Recognition engine handler
│── utils.py                # Logging, saving, formatting helpers
│── config.py               # Engine/model configuration
│── test_system.py          # Unit tests
│── requirements.txt        # Dependencies

🚀 Installation
1. Clone the repo
git clone https://github.com/your-username/speechRecognitionApp.git
cd speechRecognitionApp

2. Install dependencies
pip install -r requirements.txt

3. Install PyAudio (Windows)
pip install pipwin
pipwin install pyaudio

4. Install FFmpeg

Download from: https://www.gyan.dev/ffmpeg/builds

Extract → Add bin/ folder to PATH.

▶️ Run the App
Start the GUI:
python gui_app.py

Run unit tests:
python test_system.py

📌 Technologies Used

Python 3.x

PyAudio

SpeechRecognition

HuggingFace Transformers

Wav2Vec2

Torch

FFmpeg

GUI (tkinter)

OUTPUT:

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/e72f3a1c-2122-4a0e-9b9a-e9f48228ca14" />



🙌 Contribution

Contributions, issues, and feature requests are welcome.

🧑‍💻 Author

Mohd Jawad. B.Tech (I.T), TKR College Of Eng. & Tech., Hyderabad.
Artificial Intelligence Intern,
CodeTech IT Solutions.
