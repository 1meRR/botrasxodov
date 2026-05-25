from __future__ import annotations

import json
from typing import Optional

import pyttsx3
import speech_recognition as sr

try:
    from vosk import KaldiRecognizer, Model
except Exception:  # pragma: no cover - optional dependency at runtime
    Model = None
    KaldiRecognizer = None


class VoiceEngine:
    def __init__(self, vosk_model_path: str, use_vosk_offline: bool = True) -> None:
        self._recognizer = sr.Recognizer()
        self._tts = pyttsx3.init()
        self._tts.setProperty("rate", 180)
        self._use_vosk_offline = use_vosk_offline and Model is not None
        self._vosk_model = Model(vosk_model_path) if self._use_vosk_offline else None

    def speak(self, text: str) -> None:
        print(f"🤖 {text}")
        self._tts.say(text)
        self._tts.runAndWait()

    def listen_once(self, timeout: int = 5, phrase_time_limit: int = 8) -> Optional[str]:
        with sr.Microphone() as source:
            self._recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self._recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

        if self._use_vosk_offline and self._vosk_model:
            raw_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
            rec = KaldiRecognizer(self._vosk_model, 16000)
            rec.AcceptWaveform(raw_data)
            result = json.loads(rec.FinalResult())
            text = (result.get("text") or "").strip()
            return text or None

        try:
            text = self._recognizer.recognize_google(audio, language="ru-RU")
            return text.strip()
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None
