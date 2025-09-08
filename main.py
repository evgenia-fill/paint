import os

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.abspath(
    ".venv/lib/python3.12/site-packages/PyQt5/Qt5/plugins/platforms")

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QInputDialog
from canvas import MyGraphicsView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paint")
        self.setFixedSize(800, 600)
        self.canvas = MyGraphicsView(800, 600)
        self.setCentralWidget(self.canvas)

        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        clear_action = QAction("Clear all", self)
        clear_action.triggered.connect(self.canvas.clear_canvas)
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.canvas.save_canvas)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.canvas.exit_canvas)
        file_menu.addAction(clear_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

        tool_menu = menubar.addMenu("Tools")
        tool_pen = QAction("Pen", self)
        tool_pen.triggered.connect(self.canvas.set_pen_tool)
        tool_eraser = QAction("Eraser", self)
        tool_eraser.triggered.connect(self.canvas.set_eraser_tool)
        tool_bucket = QAction("Bucket", self)
        tool_bucket.triggered.connect(self.canvas.set_bucket_tool)
        tool_menu.addAction(tool_pen)
        tool_menu.addAction(tool_eraser)
        tool_menu.addAction(tool_bucket)

        pen_menu = menubar.addMenu("Pen")
        pen_action = QAction("Pen", self)
        pen_action.triggered.connect(self.canvas.set_pen_tool)
        pen_color_action = QAction("Color", self)
        pen_color_action.triggered.connect(lambda: self.canvas.select_color("pen"))
        set_size_action = QAction("Set size", self)
        set_size_action.triggered.connect(lambda: self.canvas.set_size("pen"))
        pen_menu.addAction(set_size_action)
        pen_menu.addAction(pen_color_action)

        eraser_menu = menubar.addMenu("Eraser")
        eraser_action = QAction("Eraser", self)
        eraser_action.triggered.connect(self.canvas.set_eraser_tool)
        set_size_action_eraser = QAction("Set size", self)
        set_size_action_eraser.triggered.connect(lambda: self.canvas.set_size("eraser"))
        eraser_menu.addAction(set_size_action_eraser)

        bucket_menu = menubar.addMenu("Bucket")
        bucket_action = QAction("Bucket", self)
        bucket_action.triggered.connect(self.canvas.set_bucket_tool)
        bucket_color_action = QAction("Color", self)
        bucket_color_action.triggered.connect(lambda: self.canvas.select_color("bucket"))
        bucket_menu.addAction(bucket_color_action)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
