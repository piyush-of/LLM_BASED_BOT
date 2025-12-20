"""
Performance test script for Annie Bot.

This script measures:
- Speech-to-text (STT) time
- LLM response time
- Text-to-speech (TTS) time
- End-to-end latency

ESP is NOT required.
"""

import time
from functions import listen, speak
import ollama

# -----------------------------
# Test configuration
# -----------------------------

TEST_TEXT = "Move forward slowly and stop after two seconds."
LLM_MODEL = "bot_annie"

# -----------------------------
# Utility
# -----------------------------

def timed(label, func, *args, **kwargs):
    """Measure execution time of a function"""
    start = time.time()
    result = func(*args, **kwargs)
    duration = time.time() - start
    print(f"[PERF] {label}: {duration:.2f} sec")
    return result, duration

# -----------------------------
# Tests
# -----------------------------

def test_stt():
    print("\n--- STT TEST ---")
    print("Speak the following sentence clearly:")
    print(f'"{TEST_TEXT}"\n')

    _, duration = timed("STT", listen)
    return duration


def test_llm():
    print("\n--- LLM TEST ---")

    def run_llm():
        return ollama.chat(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": TEST_TEXT}]
        )

    _, duration = timed("LLM", run_llm)
    return duration


def test_tts():
    print("\n--- TTS TEST ---")
    _, duration = timed("TTS", speak, TEST_TEXT)
    return duration


def test_end_to_end():
    print("\n--- END-TO-END TEST ---")

    start = time.time()

    text = TEST_TEXT
    ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": text}]
    )
    speak(text)

    duration = time.time() - start
    print(f"[PERF] End-to-end: {duration:.2f} sec")
    return duration


# -----------------------------
# Runner
# -----------------------------

if __name__ == "__main__":
    print("\n========== ANNIE PERFORMANCE TEST ==========")

    stt_time = test_stt()
    llm_time = test_llm()
    tts_time = test_tts()
    total_time = test_end_to_end()

    print("\n========== SUMMARY ==========")
    print(f"STT time       : {stt_time:.2f} sec")
    print(f"LLM time       : {llm_time:.2f} sec")
    print(f"TTS time       : {tts_time:.2f} sec")
    print(f"End-to-end     : {total_time:.2f} sec")
