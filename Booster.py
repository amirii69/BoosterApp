
import os
import subprocess
import sys
import ctypes
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtCore import Qt, QRectF

def run_as_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def enable_ultra_performance():
    subprocess.call("powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61", shell=True)
    subprocess.call("powercfg -setactive e9a42b02-d5df-448d-aa00-03f14749eb61", shell=True)

def disable_unwanted_services():
    subprocess.call("sc stop SysMain", shell=True)
    subprocess.call("sc stop WSearch", shell=True)
    subprocess.call("sc config SysMain start= disabled", shell=True)
    subprocess.call("sc config WSearch start= disabled", shell=True)

def disable_game_mode():
    subprocess.call('reg add "HKCU\\Software\\Microsoft\\GameBar" /v "AutoGameModeEnabled" /t REG_DWORD /d 0 /f', shell=True)
    subprocess.call('reg add "HKCU\\Software\\Microsoft\\GameBar" /v "GameModeEnabled" /t REG_DWORD /d 0 /f', shell=True)

class BoosterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Booster")
        self.setFixedSize(400, 400)
        self.setStyleSheet("background-color: #121212; border-radius: 20px;")
        self.is_boosted = False

        self.button = QPushButton("", self)
        self.button.setGeometry(150, 150, 100, 100)
        self.button.setStyleSheet("border-radius: 50px; background-color: red;")
        self.button.clicked.connect(self.toggle_boost)

    def toggle_boost(self):
        if not self.is_boosted:
            self.button.setStyleSheet("border-radius: 50px; background-color: green;")
            enable_ultra_performance()
            disable_unwanted_services()
            disable_game_mode()
            self.is_boosted = True
        else:
            self.button.setStyleSheet("border-radius: 50px; background-color: red;")
            self.is_boosted = False

if __name__ == '__main__':
    run_as_admin()
    app = QApplication(sys.argv)
    booster = BoosterApp()
    booster.show()
    sys.exit(app.exec_())
