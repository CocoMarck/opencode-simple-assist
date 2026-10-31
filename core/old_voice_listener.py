import json, threading, time
from typing import Callable

# Modulos
from core.vosk_manager import VoskManager
from core.microphone_recorder import MicrophoneRecorder

class OldVoiceListener:
    '''
    Escucha en bucle esperando la palabra clave y captura el comando tras detectarla.
    - Solo sirve para detectar una palabra clave.
    - Se espera que el keyword este en lower y strip.
    - Se espera un método como parámetro.
    '''
    def __init__( self, vosk_manager: VoskManager, 
        microphone_recorder: MicrophoneRecorder, keyword: str, 
        on_keyword: Callable[[], None] ):
        
        self._microphone_recorder = microphone_recorder
        self._vosk_manager = vosk_manager
        self._keyword = keyword
        self._on_keyword = on_keyword

        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._last_recognizer = None

    @property
    def grammar(self) -> list[str]:
        return [self._keyword, "[unk]"]
    
    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._loop, daemon=False, name="voice-listener")
        self._thread.start()
    
    def stop(self):
        self._stop_event.set()
        try:
            self._microphone_recorder.stop()
        except Exception:
            pass
        if self._thread:
            self._thread.join(timeout=5)
            self._thread = None
    
    def _loop(self):
        while not self._stop_event.is_set():
            if not self._wait_for_keyword():
                continue
            if self._stop_event.is_set():
                break
            self._on_keyword()
    
    def _callback(self, indata, frames, time, status):
        if status:
            print(status)
        recognizer = self._last_recognizer
        if recognizer is None:
            return
        recognizer.AcceptWaveform(indata.tobytes())
    
    def _wait_for_keyword(self) -> bool:
        recognizer = self._vosk_manager.get_recognizer(grammar=self.grammar)
        #if self._last_recognizer is None:
        self._last_recognizer = recognizer
        try:
            self._microphone_recorder.start_with_callback( self._callback )
            while not self._stop_event.is_set():
                try:
                    partial = json.loads(recognizer.PartialResult())
                    text = partial.get("partial", "").strip().lower()
                    if text == self._keyword:
                        print(f"Keyword detected: {self._keyword}")
                        self._microphone_recorder.stop()
                        return True
                except Exception:
                    pass

                time.sleep(0.01)
            return False
        finally:
            self._microphone_recorder.stop()
            del recognizer
