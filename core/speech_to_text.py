import json

# Para hablar hasta detección de silencio
import math, struct, time

# Audio
from vosk import Model, KaldiRecognizer

# Modulos
from core.vosk_manager import VoskManager
from core.microphone_recorder import MicrophoneRecorder

class SpeechToText:
    def __init__( self, vosk_manager: VoskManager, microphone_recorder: MicrophoneRecorder ):

        self._vosk_manager = vosk_manager
        self._microphone_recorder = microphone_recorder
        self._rms_threshold = None

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
    def _rms(self, data: bytes) -> float:
        '''
        Calcular RMS de int16
        '''
        if len(data) == 0:
            return 0.0
        count = len(data) // 2
        # entero corto con signo en formato little-endian
        fmt = "<%dh" % count
        samples = struct.unpack(fmt, data)
        if not samples:
            return 0.0
        sum_sq = sum(s*s for s in samples)
        return math.sqrt(sum_sq / count)
    
    def _cb(self, indata, frames, t, status) -> tuple:
        if self._rms_threshold == None:
            return
        has_spoken, last_speech = False, 0.0
        if status:
            print(status)
        data = indata.tobytes()
        # medir energia
        try:
            rms = self._rms(data)
            if rms > self._rms_threshold:
                has_spoken = True
                last_speech = time.perf_counter()
        except Exception:
            pass
        return has_spoken, last_speech

    def speech_to_text_until_silence(
        self, silence_ms: int=800, max_duration_s: int = 10, 
        rms_threshold: int = 300) -> str:
        
        recognizer = self._vosk_manager.get_recognizer() # sin gramática
        last_speech = time.perf_counter()
        has_spoken = False
        start = time.perf_counter()
        self._rms_threshold = rms_threshold

        recorder.start_with_callback(self._cb)
        try:
            while True:
                now = time.perf_counter()
                if (now -start) > max_duration_s:
                    break
                if has_spoken and ((now - last_speech) * 1000) > silence_ms:
                    break
                # Opcional: revisar partials
                try:
                    p = json.loads(recognizer.PartialResult())
                    if p.get("partial", "").strip():
                        has_spoken = True
                        last_speech = now
                except Exception:
                    pass
                time.sleep(0.01)
        finally:
            time.sleep(0.01)
            self._microphone_recorder.stop()
        
        try:
            res = json.load(recognizer.FinalResult())
            return res.get("text", "").strip()
        except Exception:
            return ""
        finally:
            del recognizer

    
