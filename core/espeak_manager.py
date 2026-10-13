import os

class EspeakManager:
    def __init__(self):
        pass
    
    def speak(self, text: str):
        espeak_command = f"espeak-ng -v es '{text}'"
        print(espeak_command)
        os.system(espeak_command)