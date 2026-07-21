"""Core audio output - Offline TTS via pyttsx3."""

import pyttsx3


class Speaker:
    """Speaks text aloud offline using pyttsx3 (SAPI5 on Windows)."""

    def __init__(self, rate: int = 175, volume: float = 1.0):
        self._engine = pyttsx3.init()
        self._engine.setProperty("rate", rate)
        self._engine.setProperty("volume", volume)
        self._select_voice()

    def _select_voice(self):
        voices = self._engine.getProperty("voices")
        for v in voices:
            if "male" in v.name.lower() or "david" in v.name.lower():
                self._engine.setProperty("voice", v.id)
                return

    def speak(self, text: str):
        self._engine.say(text)
        self._engine.runAndWait()

    def set_rate(self, rate: int):
        self._engine.setProperty("rate", rate)

    def set_volume(self, volume: float):
        self._engine.setProperty("volume", max(0.0, min(1.0, volume)))
