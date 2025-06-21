from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout,
    QHBoxLayout, QMessageBox, QLabel
)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt
from blackJack_GUI import *
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = BlackJackGUI()
    win.show()
    sys.exit(app.exec())
