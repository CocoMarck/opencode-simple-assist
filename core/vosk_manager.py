import json

# Audio
from vosk import Model, KaldiRecognizer

class VoskManager:
    '''
    - model: Modelo vosk. Carpeta con binarios.
    - sample_rate: Esto es del micrófono, el como lo grabas.
    '''
    def __init__(self, model: Model, sample_rate: float ):
        self.model = model
        self.sample_rate = sample_rate

    def get_recognizer(self, grammar: list[str] | None = None) -> KaldiRecognizer:
        recognizer = KaldiRecognizer(self.model, self.sample_rate)
        if grammar is not None:
            recognizer.SetGrammar(json.dumps(grammar))
        recognizer.SetWords(False)
        return recognizer