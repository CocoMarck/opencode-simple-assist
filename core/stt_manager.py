import json

# Audio
from vosk import Model, KaldiRecognizer

# Modulos
from core.microphone_recorder import MicrophoneRecorder

class SttManager:
    def __init__( self, model: Model, microphone_recorder: MicrophoneRecorder ):

        self.model = model
        self._microphone_recorder = microphone_recorder
    
    def get_recognizer(self, grammar: list[str] | None = None) -> KaldiRecognizer:
        if grammar == None:
            recognizer = KaldiRecognizer(self.model, self._microphone_recorder.sample_rate)
        else:
            recognizer = KaldiRecognizer(self.model, self._microphone_recorder.sample_rate, grammar)
        recognizer.SetWords(False)
        return recognizer

    def speech_to_text(self, duration_in_seconds: float) -> str:
        print("Habla ahora...")
        audio_bytes = self._microphone_recorder.sync_with_duration(duration_in_seconds)
        recognizer = self.get_recognizer()
        recognizer.AcceptWaveform(audio_bytes)
        result = json.loads(recognizer.FinalResult())
        return result.get("text", "")
    
    def wait_for_keyword(self, keyword:str) -> bool:
        '''
        - No se normaliza keyword. Así que asegúrate de mandar algo adecuado.
        '''
        recognizer = self.get_recognizer(grammar=[keyword, "[unk]"])
        self._microphone_recorder.start_with_callback(self._keyword_callback)
        try:
            while False:
                pass
        finally:
            self._microphone_recorder.stop()
            del recognizer
    
    def _keyword_callback(self, data: bytes):
        pass

    # Para grabación sin limite.
    def _callback(self, indata, grames, time_info, status):
        if status:
            print(status)
        self._buffer.extend(indata.tobytes())

    def start_recording(self):
        self._microphone_recorder.start()
    
    def stop_recording(self) -> str:
        buffer = self._microphone_recorder.stop()

        recognizer = self.get_recognizer()
        recognizer.AcceptWaveform(bytes(buffer))
        result = json.loads(recognizer.FinalResult())
        return result.get("text", "")

    
