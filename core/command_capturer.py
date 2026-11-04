import json, time, struct, math
from typing import Optional

# Modulos
from core.vosk_manager import VoskManager
from core.microphone_recorder import MicrophoneRecorder

class CommandCapturer:
    def __init__(
        self, vosk_manager: VoskManager, microphone_recorder: MicrophoneRecorder,
        silence_ms: int=800, min_speech_ms: int=250, max_duration_s: int=10,
        rms_threshold: int=300):
    
        self._vosk_manager = vosk_manager
        self._microphone_recorder = microphone_recorder
        self.silence_ms = silence_ms
        self.min_speech_ms = min_speech_ms
        self.max_duration_s = max_duration_s
        self.rms_threshold = rms_threshold

        # Estado para la captura actual
        self._recognizer = None
        self._last_speech = 0.0
        self._first_speech = None
        self._speaking = False
        self._start_time = 0.0

    def _rms(self, data: bytes) -> float:
        '''
        Calcular RMS de int16
        '''
        if len(data) == 0: return 0.0
        count = len(data)//2
        samples = struct.unpack("<%dh"%count, data)
        if not samples: return 0.0
        sum_sq = sum(s*s for s in samples)
        return math.sqrt( sum_sq/len(samples) )
    
    def _on_audio(self, indata, frames, time_info, status):
        if status:
            print(status)
        if self._recognizer is None:
            return
        
        data = indata.tobytes()

        # Medir energía para detecta voz
        rms = self._rms(data)
        now = time.perf_counter()
        if rms > self.rms_threshold:
            if not self._speaking:
                self._speaking = True
                self._first_speech = now
            self._last_speech = now
        
        # Alimentar a Vosk
        try:
            self._recognizer.AcceptWaveform(data)
        except Exception as e:
            print(e)
    
    def capture(self) -> str:
        '''
        Sync. Bloquea todo.
        '''
        # Crear recognizer sin gramática para transcribir el comando
        self._recognizer = self._vosk_manager.get_recognizer()
        self._speaking = False
        self._first_speech = None
        self._last_speech = time.perf_counter()
        self._start_time = time.perf_counter()

        # Empezar a grabar
        self._microphone_recorder.start_with_callback(self._on_audio)

        try:
            while True:
                now = time.perf_counter()
                elapsed_total = now - self._start_time

                # Límite máximo de seguridad
                if elapsed_total > self.max_duration_s:
                    break
                
                # No empezar a contar silencio hasta haber hablado al menos un poco
                if self._speaking and self._first_speech is not None:
                    elapsed_since_first = now - self._first_speech
                    if elapsed_since_first < (self.min_speech_ms / 1000.0):
                        time.sleep(0.01)
                        continue
                    
                    # Contar silencio desde la última vez que hubo voz
                    if (now -self._last_speech) * 1000 >= self.silence_ms:
                        break
                
                time.sleep(0.01)
        finally:
            # Cortar feed ANTES de finalizar el recognizer
            # Para obtener ultima palabra
            self._microphone_recorder.clear_external_callback()
            time.sleep(0.01)
            self._microphone_recorder.stop()
        
        text = ""
        try:
            if self._recognizer is not None:
                result = json.loads(self._recognizer.FinalResult())
                text = result.get("text", "").strip()
        except Exception as e:
            print(e)
        finally:
            self._recognizer = None
            self._speaking = False
            self._first_speech = None
        return text