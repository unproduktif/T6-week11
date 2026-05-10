# Nama  : Dodi Wijaya
# NIM   : F1D02310047
# Kelas : (Isi Kelas)

import sys
import os

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

app = QApplication(sys.argv)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
style_path = os.path.join(BASE_DIR, "styles", "style.qss")

with open(style_path, "r") as f:
    app.setStyleSheet(f.read())

window = MainWindow()
window.show()

sys.exit(app.exec())