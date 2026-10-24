import json

# Audio
from vosk import Model, KaldiRecognizer
import sounddevice

class SttManager:
    def __init__( 
        self, model: Model, sample_rate: int, duration_in_seconds: int):

        self.model = model
        self._sample_rate = sample_rate
        self._duration_in_seconds = duration_in_seconds
    
    def set_duration(self, duration: int):
        if not isinstance(duration, int):
            raise Exception("The duration need a int value.")
        self._duration_in_seconds = duration
    
    def get_recognizer(self) -> KaldiRecognizer:
        recognizer = KaldiRecognizer(self.model, self._sample_rate)
        recognizer.SetWords(False)
        return recognizer
    
    def _get_duration(self):
        return int(self._duration_in_seconds * self._sample_rate)

    def speech_to_text(self) -> str:
        print("Habla ahora...")
        audio = sounddevice.rec(
            self._get_duration(),
            samplerate=self._sample_rate,
            channels=1,
            dtype="int16",
            device=None
        )
        sounddevice.wait()
        recognizer = self.get_recognizer()
        if recognizer.AcceptWaveform(audio.tobytes()):
            pass

        result = json.loads(recognizer.FinalResult())
        return result.get("text", "").strip()