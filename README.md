# Annie Bot

**Annie** is a playful, voice-controlled differential-drive robot powered by **local LLMs**.  
She listens to you, talks back using offline text-to-speech, and moves around by sending motion commands to an ESP-based robot.  
If the ESP is unavailable, Annie continues running without crashing.

The “brain” of Annie is a locally hosted Ollama model (`bot_annie`) that generates:
- conversational responses
- motion commands in the format:

```
[linear_velocity, angular_velocity, duration]
```

---

## ✨ Features

- 🎤 **Voice-controlled**  
  Offline speech recognition using Whisper (`faster-whisper`).

- 🔊 **Speaks back locally**  
  Uses **Piper TTS** (fully offline, no cloud APIs).

- 🛞 **Robot movement**  
  Sends motion commands to an ESP8266 / ESP32 over Wi-Fi.

- 🧠 **Local LLM reasoning**  
  Powered by Ollama — no OpenAI, no internet required after setup.

- 🔌 **Graceful fallback**  
  If the ESP is unreachable, Annie continues running without crashing.

- 🖥️ **Cross-platform**  
  Works on **Linux** and **Windows** (minor audio setup differences).

---

## 📦 Requirements Overview

Annie has **three kinds of dependencies**:

1. Python libraries (installed via `pip`)
2. System / audio libraries (installed via OS package manager)
3. External binaries (manual install)

---

## 🐍 Python Dependencies (Linux & Windows)

Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
```

### Linux
```bash
source .venv/bin/activate
```

### Windows (PowerShell)
```powershell
.venv\Scripts\Activate.ps1
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔊 System / Audio Dependencies

### 🐧 Linux (Required)

```bash
sudo apt update
sudo apt install -y \
    libportaudio2 \
    portaudio19-dev \
    libportaudiocpp0
```

### 🪟 Windows

No manual system packages are required.
### Windows Audio Notes

- Make sure your microphone is enabled:
  - Settings → Privacy → Microphone
  - Allow apps to access microphone

- If audio playback fails, install:
  - Microsoft Visual C++ Redistributable (x64)

No additional system libraries are required on Windows.

---

## 🔊 Piper TTS (External Binary – Required)

Download Piper manually from:  
https://github.com/rhasspy/piper/releases

Place the extracted `piper/` directory inside the project root.

---

## 🎙️ Piper Voice Models (Required)

Download a voice model from:  
https://github.com/rhasspy/piper/blob/master/VOICES.md

Place it in:

```
piper-voices/
```

---

## 🧠 Ollama Model Setup

```bash
cd models
ollama pull mistral
ollama create bot_annie -f ./bot_annie_model_file
```

---

## 🚀 Running Annie

```bash
python mind.py
```

---

## 📡 ESP Setup

- **Wi-Fi SSID:** Annie  
- **Password:** 12345678  

---

## ⏹ Stopping Annie

Press `CTRL + Z` or  `CTRL + C` on linux
Press `CTRL + C` on windows

---

## 🛠 Credits

- faster-whisper
- Piper TTS
- Ollama