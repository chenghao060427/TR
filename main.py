import sys
from PyQt5.QtWidgets import QMainWindow,QDesktopWidget,QApplication,QInputDialog,QStatusBar
from gui.m_window import m_window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = m_window()
    main.show()
    sys.exit(app.exec_())
