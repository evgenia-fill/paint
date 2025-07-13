import os

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.abspath(
    ".venv/lib/python3.12/site-packages/PyQt5/Qt5/plugins/platforms")

import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QMainWindow, QGraphicsScene
from PyQt5.QtGui import QColor
from canvas import MyGraphicsView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paint")
        self.setGeometry(100, 100, 800, 600)
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QColor("white"))
        self.view = MyGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
