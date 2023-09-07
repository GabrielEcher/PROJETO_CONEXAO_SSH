from PySide6.QtWidgets import QWidget, QGridLayout, QMainWindow, QTextEdit
from PySide6.QtGui import QIcon
from variables import WINDOW_ICON_PATH


class WindowErr(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        icon = QIcon(str(str(WINDOW_ICON_PATH)))
        status_base = 'ERRO INESPERADO AO CONECTAR-SE À BASE TESTE WMS,\nCONTATE O SUPORTE!'

        # Widget do status
        self.setWindowTitle('ERRO')
        self.status_text_edit = QTextEdit(status_base)
        self.status_text_edit.setReadOnly(True)
        status_text_style = "border: 2px solid white; padding 5px; font-size 20px; color: orange;"
        self.status_text_edit.setStyleSheet(status_text_style)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)        
        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)
        self.setWindowIcon(icon)
        self.layout.addWidget(self.status_text_edit, 1, 0, 1, 2)
        
        
    

    