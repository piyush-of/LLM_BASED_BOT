from datetime import datetime
import subprocess
from time import sleep
import sounddevice as sd
import numpy as np
import subprocess
import os
from faster_whisper import WhisperModel
import tempfile
import scipy.io.wavfile as wav
import re
import noisereduce as nr
import platform

class SimpleTwist:
    def __init__(self):
        self.linear = type("vec", (), {"x": 0.0, "y": 0.0, "z": 0.0})()
        self.angular = type("vec", (), {"x": 0.0, "y": 0.0, "z": 0.0})()

MESSAGE = SimpleTwist()

PIPER_MODEL = os.path.expanduser("piper-voices/en_US-hfc_female-medium.onnx")
model = WhisperModel("small.en", device="cuda", compute_type="float16")

# List of actions...


def idle():
    MESSAGE.linear.x = 0.0
    MESSAGE.linear.y = 0.0
    MESSAGE.linear.z = 0.0

    MESSAGE.angular.x = 0.0
    MESSAGE.angular.y = 0.0
    MESSAGE.angular.z = 0.0


############################################################

def twist(x: float, z: float, time: float):
    '''Moves the bot in the specified linear x and angular z direction for the specified time. The bot will move infinitely if time is negative.'''
    """
    SIMULATION-ONLY:
    Used when SIM=True or ESP is unreachable.
    Currently unused in normal ESP operation.
    """

    MESSAGE.linear.x = x
    MESSAGE.linear.y = 0.0
    MESSAGE.linear.z = 0.0

    MESSAGE.angular.x = 0.0
    MESSAGE.angular.y = 0.0
    MESSAGE.angular.z = z
    

    if time < 0:
        return
    
    sleep(time)

    idle()


def play_beep(frequency=1000, duration=0.2, samplerate=16000):
    """Play a beep sound"""
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    sd.play(wave, samplerate)
    sd.wait()



def listen(show=True) -> str:
    duration = 5
    samplerate = 16000

    play_beep(frequency=880, duration=0.25)

    print("\rListening...", end="", flush=True)

    # Record
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()

    # Convert to float32 for processing
    audio_float = audio.astype(np.float32)

    # Apply noise reduction
    reduced = nr.reduce_noise(y=audio_float.flatten(), sr=samplerate)

    # Save to temp wav
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        wav.write(tmpfile.name, samplerate, reduced.astype(np.int16))  # convert back to int16
        tmp_path = tmpfile.name

    # Transcribe
    segments, _ = model.transcribe(tmp_path)
    text = " ".join([seg.text for seg in segments]).strip()

    text = re.sub(r"[^a-zA-Z0-9 ,.\[\]\-_]", "", text)

    if show and text:
        print("\rYOU:", end=" ")
        print("\033[92m" + text + "\033[0m \n")

    return text

    
def speak(text: str):
    if not text or not text.strip():
        return

    print("\033[94m" + text + "\033[0m")

    allowed_chars = re.compile(r'[^a-zA-Z0-9 .,!?\'\"]')
    filtered = allowed_chars.sub('', text)

    if not filtered.strip():
        print("No speakable content after filtering")
        return

    try:

        if platform.system() == "Windows":
            PIPER_BIN = os.path.abspath("piper/piper.exe")
        else:
            PIPER_BIN = os.path.abspath("piper/piper")
        process = subprocess.Popen(
            [PIPER_BIN , "--model", PIPER_MODEL, "--output-raw", "--length-scale", "1.1"]
,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )

        process.stdin.write(filtered.encode("utf-8"))
        process.stdin.close()

        audio = process.stdout.read()
        process.wait()

        audio_data = np.frombuffer(audio, dtype=np.int16).astype(np.float32) / 32768.0
        sd.play(audio_data, samplerate=22050)
        sd.wait()

    except Exception as e:
        print("Piper TTS error:", e)
