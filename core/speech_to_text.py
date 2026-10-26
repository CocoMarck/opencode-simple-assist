import json

# Audio
from vosk import Model, KaldiRecognizer

# Modulos
from core.vosk_manager import VoskManager
from core.microphone_recorder import MicrophoneRecorder

class SpeechToText:
    def __init__( self, vosk_manager: VoskManager, microphone_recorder: MicrophoneRecorder ):

        self._vosk_manager = vosk_manager
        self._microphone_recorder = microphone_recorder

    def start_recording(self):
        self._microphone_recorder.start()
    
    def stop_recording(self) -> str:
        buffer = self._microphone_recorder.stop()

        recognizer = self._vosk_manager.get_recognizer()
        print("recognizer paso")
        recognizer.AcceptWaveform(bytes(buffer))
        result = json.loads(recognizer.FinalResult())
        return result.get("text", "")

    
