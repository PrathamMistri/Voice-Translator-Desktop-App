

# 🎙️ Real-Time Voice Translator 🔊

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Issues](https://img.shields.io/github/issues/your-username/real-time-voice-translator)
![Stars](https://img.shields.io/github/stars/your-username/real-time-voice-translator?style=social)

---

## 📖 Description
A desktop-based Real-Time Voice Translator app built in Python with Tkinter.  
It converts spoken English into **two user-selected languages**, displaying both translated text and audio output in real time.  
Uses **SpeechRecognition**, **deep-translator** (Google Translate API), and **gTTS** for text-to-speech output.

---

## ✨ Features
- 🎤 Live Speech Recognition (English input)  
- 🌐 Translate into multiple languages simultaneously  
- 🔊 Real-time audio playback of translations  
- 🖥 Tkinter GUI with Dark/Light theme toggle  
- ⚙ Configurable settings saved in `config.json`  
- 📝 Tooltips for guidance on buttons  
- 🧹 Clear input/output fields with a single click  

---

## ⚡ Installation

1. **Clone the repository**  
```bash
git clone https://github.com/your-username/real-time-voice-translator.git
cd real-time-voice-translator
```

2. **Install dependencies**  
```bash
pip install -r requirements.txt
```

3. **Run the app**  
```bash
python app.py
```

### PyAudio (Microphone Support)
- **Windows**:  
```bash
pip install pipwin
pipwin install pyaudio
```
- **Linux (Debian/Ubuntu)**:  
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```
- **macOS**:  
```bash
brew install portaudio
pip install pyaudio
```

---

## 📂 Project Structure

```
real-time-voice-translator/
│── app.py
│── utils.py
│── requirements.txt
│── LICENSE
│── README.md
│
├── config/
│   └── settings.json
├── assets/
│   ├── icon.ico
│   └── screenshots/
├── audio/
│   ├── voice1.mp3
│   └── voice2.mp3
└── docs/
    └── presentation.pptx
```

---

## 📜 License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---
