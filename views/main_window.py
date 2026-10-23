from pathlib import Path
from PyQt6 import QtWidgets, uic

# SimpleAssist
from core.simple_assist import SimpleAssist

class MainWindow( QtWidgets.QMainWindow ):
    def __init__(self, ui_file: Path, simple_assist: SimpleAssist):
        super().__init__()

        uic.loadUi(ui_file, self)
        
        self._simple_assist = simple_assist

        # Widgets: `button_send, entry_input`
        self.button_send.clicked.connect( self._assist_request )
    
    def _assist_request(self):
        text = self.entry_input.text().strip()
        if not text:
            return    
        self._simple_assist.request(text)