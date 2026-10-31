'''
Claude code
'''
import json
import queue
import threading
import time
from enum import Enum, auto
from typing import Callable

# Modulos
from core.vosk_manager import VoskManager
from core.microphone_recorder import MicrophoneRecorder

class _State(Enum):
    WAITING_KEYWORD = auto()
    CAPTURING_COMMAND = auto()

class VoiceListener:
    '''
    Escucha en bucle esperando la palabra clave y captura el comando tras detectarla.
    - Solo sirve para detectar una palabra clave.
    - Se espera que el keyword este en lower y strip.
    - Se espera un método como parámetro.
    - NO hacer `stop()` dentro del `on_command`. Haría un join dentro de si mismo (por el hilo worker).
    - El command recibe puede recibir una palabra mocha, pero recibe algo, es porque se detecto la keyword.
    '''
    def __init__(
        self, microphone_recorder: MicrophoneRecorder, 
        vosk_manager: VoskManager, keyword: str, on_command: Callable[[str], None], command_timeout: float = 8.0):

        self.microphone_recorder = microphone_recorder
        self.vosk_manager = vosk_manager
        self.keyword = keyword.strip().lower()
        self.on_command = on_command
        self.command_timeout = command_timeout

        self._queue: queue.Queue[bytes] = queue.Queue(maxsize=200)
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
    
    # --- Hilo de audio: solo encola ---
    def _on_audio(self, indata, frames, time_info, status):
        try:
            self._queue.put_nowait(indata.tobytes())
        except queue.Full:
            pass # Mejor perder un bloque a bloquear el hilo de audio
    
    # --- Hilo worker ---
    def _run(self):
        state = _State.WAITING_KEYWORD
        keyword_rec = self.vosk_manager.get_recognizer([self.keyword, "[unk]"])
        command_rec = None
        deadline = 0.0

        while not self._stop_event.is_set():
            # Timeout del comando
            if state is _State.CAPTURING_COMMAND and time.monotonic() > deadline:
                text = json.loads(command_rec.FinalResult()).get("text", "").strip()
                if text:
                    self._dispatch(text)
                state = self._back_to_waiting(keyword_rec)
                continue
            
            try:
                data = self._queue.get(timeout=0.2)
            except queue.Empty:
                continue
        
            if state is _State.WAITING_KEYWORD:
                if keyword_rec.AcceptWaveform(data):
                    text = json.loads(keyword_rec.Result()).get("text", "")
                else:
                    text = json.loads(keyword_rec.PartialResult()).get("partial", "")
            
                if self.keyword in text:
                    command_rec = self.vosk_manager.get_recognizer()
                    deadline = time.monotonic() + self.command_timeout
                    state = _State.CAPTURING_COMMAND
        
            else: # CAPTURING_COMMAND
                if command_rec.AcceptWaveform(data):
                    text = json.loads(command_rec.Result()).get("text", "").strip()
                    if text:
                        self._dispatch(text)
                        state = self._back_to_waiting(keyword_rec)

    def _back_to_waiting(self, keyword_rec) -> _State:
        keyword_rec.Reset()
        with self._queue.mutex:
            self._queue.queue.clear()
        return _State.WAITING_KEYWORD
    
    def _dispatch(self, text: str):
        try:
            self.on_command(text)
        except Exception as e:
            print(f"Error in on_command: {e}")
    
    # --- API pública ---
    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        self.microphone_recorder.start_with_callback(self._on_audio)
    
    def stop(self):
        self._stop_event.set()
        self.microphone_recorder.stop()
        if self._thread:
            self._thread.join(timeout=2)
