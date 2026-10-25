from pathlib import Path
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QThread, pyqtSignal

# SimpleAssist
from core.simple_assist import SimpleAssist
from core.stt_manager import SttManager

# STT
class SttWorker(QThread):
    finished = pyqtSignal(str)
    def __init__(self, stt_manager: SttManager, parent=None):
        super().__init__(parent)
        self._stt_manager = stt_manager
    
    def run(self):
        text = self._stt_manager.stop_recording()
        self.finished.emit(text)

# MainWindow
class MainWindow( QtWidgets.QMainWindow ):
    def __init__(self, ui_file: Path, simple_assist: SimpleAssist, stt_manager: SttManager):
        super().__init__()

        uic.loadUi(ui_file, self)
        
        self._simple_assist = simple_assist
        self._stt_manager = stt_manager
        self._worker = None

        # Widgets: `button_send, textedit_input, button_speech`
        self.button_send.clicked.connect( self._assist_request )
        self.button_speech.setCheckable(True)
        self.button_speech.toggled.connect( self._speech_toggle )
    
    def _assist_request(self):
        text = self.textedit_input.toPlainText().strip()
        if not text:
            return    
        self._simple_assist.request(text)
    
    # STT
    def _speech_toggle(self, checked: bool):
        if checked:
            self.button_send.setEnabled(False)
            self._stt_manager.start_recording()
            return
        
        self.button_send.setEnabled(True)

        self._worker = SttWorker(self._stt_manager, self)
        self._worker.finished.connect(self._on_speech_done)
        self._worker.finished.connect(self._on_worker_finished)
        self._worker.start()
    
    def _on_speech_done(self, text: str):
        if not text:
            self.statusBar().showMensagge("No se detecto vóz, 2000")
            return

        input_text = self.textedit_input.toPlainText().strip()
        if input_text.replace(" ", "") == "":
            self.textedit_input.setPlainText(text)
        else:
            self.textedit_input.setPlainText(input_text + f" {text}")
    
    def _on_worker_finished(self):
        if self._worker is not None:
            self._worker.deleteLater()
            self._worker = None
