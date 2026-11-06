import json

# Para hablar hasta detección de silencio
import math, struct, time

# Audio
from vosk import Model, KaldiRecognizer

# Modulos
from core.vosk_manager import VoskManager
from core.microphone_recorder import MicrophoneRecorder
from core.command_capturer import CommandCapturer

class SpeechToText:
    def __init__( self, vosk_manager: VoskManager, microphone_recorder: MicrophoneRecorder ):

        self._vosk_manager = vosk_manager
        self._microphone_recorder = microphone_recorder
        self._rms_threshold = None
        self._command_capturer = CommandCapturer(
            self._vosk_manager, self._microphone_recorder, 
            silence_ms=1000, max_duration_s=60)

    def start_recording(self):
        self._microphone_recorder.start()
    
    def stop_recording(self) -> str:
        buffer = self._microphone_recorder.stop()

        recognizer = self._vosk_manager.get_recognizer()
        print("Recognizer pass")
        recognizer.AcceptWaveform(bytes(buffer))
        result = json.loads(recognizer.FinalResult())
        return result.get("text", "")
    
    def sync_recording_with_seconds(self, seconds: float) -> float:
        audio_bytes = self._microphone_recorder.sync_with_seconds(seconds)
        recognizer = self._vosk_manager.get_recognizer()
        recognizer.AcceptWaveform(audio_bytes)
        result = json.loads(recognizer.FinalResult())
        return result.get("text", "")
    
    # Hablar hasta detección de silencio
    def speech_to_text_until_silence(self) -> str:
        return self._command_capturer.capture()

    
