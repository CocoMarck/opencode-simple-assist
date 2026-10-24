from vosk import Model, KaldiRecognizer
import json, time
from pathlib import Path
import sounddevice as sd

LOG_FILE = Path("./test_vosk.log")
DURATION_IN_SECONDS = 6
SAMPLE_RATE = 16000

def main():
    print("Cargando modelo...")
    model = Model("./models/vosk-model-small-es-0.42")
    rec = KaldiRecognizer(model, SAMPLE_RATE)
    rec.SetWords(False)
    print("Modelo cargado correctamente")

    # Graba desde el dispositivo por defecto
    print(f"Usando micrófono por defecto. Grabando {DURATION_IN_SECONDS} segundos...")
    print("Habla ahora...")
    audio = sd.rec(
        int(DURATION_IN_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        device=None
    )
    sd.wait()
    print("Grabación finalizada. Transcribiendo...")

    # Vosk espera bytes int16
    if rec.AcceptWaveform(audio.tobytes()):
        pass

    result = json.loads(rec.FinalResult())
    text = result.get("text", "").strip()

    if not text:
        print("")
    else:
        print("")
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {text}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)
    print(f"Guardado en {LOG_FILE}")

if __name__ == "__main__":
    main()
    
