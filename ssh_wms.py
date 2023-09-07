import sys
import ctypes
import paramiko
from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QGridLayout, QMainWindow, QLabel, QTextEdit
from threading import Event
from PySide6.QtGui import QIcon
from variables import WINDOW_ICON_PATH
from styles import setupTheme
from err_window import WindowErr
ADDRESS = '0.0.0.0'
USERNAME = 'root'
PASSWORD = 'password'



class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        icon = QIcon(str(str(WINDOW_ICON_PATH)))
        self.status_bs = True
        self.status_output = ''
        
        # Botões
        
        self.start_button = QPushButton('Ligar base teste WMS')
        self.stop_button = QPushButton('Desligar base teste WMS')
        self.restart_button = QPushButton('Reiniciar base teste WMS')
        self.status_button = QPushButton('Ver status da base')
        
        button_font_color = "font-size: 14px; color: orange;"
        self.start_button.setStyleSheet(button_font_color)
        self.stop_button.setStyleSheet(button_font_color)
        self.restart_button.setStyleSheet(button_font_color)
        self.status_button.setStyleSheet(button_font_color)
        
        # Widget do status
        self.status_label = QLabel('Status da base:')
        self.status_text_edit = QTextEdit()
        self.status_text_edit.setReadOnly(True)
        status_text_style = "border: 2px solid white; padding 5px; font-size 16px; color: orange;"
        self.status_text_edit.setStyleSheet(status_text_style)
        
        # Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle('Gerenciador base WMS')
        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)
        self.setWindowIcon(icon)
        
        
        self.layout.addWidget(self.status_label, 0, 0, 1, 2)
        self.layout.addWidget(self.status_text_edit, 1, 0, 1, 2)
        self.layout.addWidget(self.status_button, 2, 0, 1, 2)
        self.layout.addWidget(self.start_button, 3, 0, 1, 1)
        self.layout.addWidget(self.stop_button, 3, 1, 1, 1)
        self.layout.addWidget(self.restart_button, 4, 0, 1, 2)
        
        # Triggers
     
        self.start_button.clicked.connect(self.start_base)
        self.status_button.clicked.connect(self.status_base)
        self.stop_button.clicked.connect(self.stop_base)
        self.restart_button.clicked.connect(self.restart_base)
    
    def show_loading_message(self, message):
        loading_html = f'<p>{message}</p><p><progress></progress></p>'
        self.status_text_edit.setHtml(loading_html)
        self.status_text_edit.repaint()
        
    
    def status_base(self):
        
        stdin, stdout, stderr = ssh.exec_command('systemctl status glassfish.service')
        stdin.close()
        
        for line in stdout.readlines():
            result = line.replace('\n', '')
            if 'Active: active' in line:
                self.status_output += 'Base teste WMS ativa\n'
                self.status_bs = True
                
            elif 'Active: inactive' in line:
                self.status_output += 'Base inativa\n'
                self.status_bs = False
                
            
        self.status_text_edit.setPlainText(self.status_output)
                
    def start_base(self):
        
        if not self.status_bs:
            self.show_loading_message('Ativando base teste WMS...')
            stdin, stdout, stderr = ssh.exec_command('systemctl start glassfish.service && systemctl status glassfish.service')
            
            Event().wait(60)
            
            stdin, stdout, stderr = ssh.exec_command('systemctl status glassfish.service')
            for line in stdout.readlines():
                result = line.replace('\n', '')
                if 'Active: active' in line:
                    self.status_text_edit.setPlainText('Base ativa!')
                elif 'Active: inactive' in line:
                    self.status_text_edit.setPlainText('Não foi possível ativar a base\nContate o suporte!')
            
        elif self.status_bs:
            self.status_text_edit.setPlainText('Base já está ativa!')
        
    def stop_base(self):
        
        if self.status_bs:
            self.show_loading_message('Desativando base teste WMS...')
            stdin, stdout, stderr = ssh.exec_command('systemctl stop glassfish.service && systemctl status glassfish.service')
            
            Event().wait(10)
            
            for line in stdout.readlines():
                result = line.replace('\n', '')
                if 'Active: inactive' in line:
                    self.status_text_edit.setPlainText('Base desativada com sucesso!')
                elif 'Active: active' in line:
                    self.status_text_edit.setPlainText('Não foi possível desativar a base\nContate o suporte!')
      
        elif not self.status_bs:
            self.status_text_edit.setPlainText('Base já está inativa!')       
        
        
    def restart_base(self):
        
        stdin, stdout, stderr = ssh.exec_command('systemctl restart glassfish.service && systemctl status glassfish.service')
        self.show_loading_message('Reiniciando base teste WMS...')
        
        Event().wait(60)
        
        
        for line in stdout.readlines():
            result = line.replace('\n', '')
            if 'Active: active' in line:
                self.status_text_edit.setPlainText('Base reiniciada!')           
            elif 'Active: inactive' in line:
                self.status_text_edit.setPlainText('Erro ao tentar reiniciar\nContate o suporte!')
  
    

if __name__ == '__main__':
    idapp = u"conexao_ssh_wms"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(idapp)
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ADDRESS, username=USERNAME, password=PASSWORD)
        app = QApplication(sys.argv)
        setupTheme()
        window = Window()
        window.show()
        sys.exit(app.exec()) # Loop da aplicação
    
    except:
        app2 = QApplication(sys.argv)
        setupTheme()
        window2 = WindowErr()
        window2.show()
        sys.exit(app2.exec())
    
        
            
    