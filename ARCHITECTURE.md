# Annie Bot – Architecture Overview

## High-level flow

Mic → Speech Recognition → LLM → Action Parser → ESP → Motors
                          ↓
                        Piper TTS → Speakers

## Core files

- mind.py
  - Main control loop
  - Handles listening, thinking, acting

- functions.py
  - listen(): speech-to-text
  - speak(): text-to-speech
  - send_twist(): ESP communication

## What NOT to touch first
- Core logic in mind.py
- ESP communication format

## Good areas for beginners
- improving prompt
- improving speech filters
- adding logging
- improving error handling

## 📁 Project Structure

```text
bot-annie/
├── mind.py              # Main control loop
├── functions.py         # Speech, TTS, ESP communication
├── perf_test.py         # Performance benchmarking script
├── ARCHITECTURE.md      # System architecture & code overview
├── CONTRIBUTING.md      # Contribution rules & guidelines
├── README.md            # Project overview & setup
├── requirements.txt     # Python dependencies
├── .gitignore           # Git ignore rules
├── ESP Code/            # ESP8266 / ESP32 firmware
├── piper/               # (ignored) Piper TTS binary
├── piper-voices/        # (ignored) Piper voice models
├── models/              # LLM / STT models (if any)
├── log/                 # Logs
└── __pycache__/         # Python cache (ignored)

```
## 🔧 functions.py – Core Utilities

This file contains reusable helper functions.

### Speech functions
- `listen()`
  - Records audio from microphone
  - Converts speech to text using Whisper

- `speak(text)`
  - Converts text to speech using Piper
  - Plays audio using sounddevice

### Motion / ESP functions
- `send_twist(lin, ang, dur)`
  - Sends motion command to ESP via HTTP
  - Non-blocking

### Utility functions
- `filter_text(text)`
  - Cleans text before TTS
