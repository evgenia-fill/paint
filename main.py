import os

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.abspath(
    ".venv/lib/python3.12/site-packages/PyQt5/Qt5/plugins/platforms")

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction
from canvas import MyGraphicsView
from functions import Functions


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paint")
        self.setFixedSize(800, 600)
        self.canvas = MyGraphicsView(800, 600)
        self.setCentralWidget(self.canvas)
        self.functions = Functions(self.canvas)

        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        clear_action = QAction("Clear all", self)
        clear_action.triggered.connect(self.functions.clear_canvas)
        save_action = QAction("Save file", self)
        save_action.triggered.connect(self.functions.save_canvas)
        exit_action = QAction("Load file", self)
        exit_action.triggered.connect(self.functions.load_canvas)
        file_menu.addAction(clear_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

        tools_menu = menubar.addMenu("Tools")
        tool_pen = QAction("Pen", self)
        tool_pen.triggered.connect(self.canvas.set_pen_tool)
        tool_eraser = QAction("Eraser", self)
        tool_eraser.triggered.connect(self.canvas.set_eraser_tool)
        tool_bucket = QAction("Bucket", self)
        tool_bucket.triggered.connect(self.canvas.set_bucket_tool)
        tools_menu.addAction(tool_pen)
        tools_menu.addAction(tool_eraser)
        tools_menu.addAction(tool_bucket)

        shapes_menu = menubar.addMenu("Shapes")
        shapes_line = QAction("Line", self)
        shapes_line.triggered.connect(self.canvas.set_line_tool)
        shapes_rect = QAction("Rectangle", self)
        shapes_rect.triggered.connect(self.canvas.set_rect_tool)
        shapes_ellipse = QAction("Ellipse", self)
        shapes_ellipse.triggered.connect(self.canvas.set_ellipse_tool)
        shapes_menu.addAction(shapes_line)
        shapes_menu.addAction(shapes_rect)
        shapes_menu.addAction(shapes_ellipse)

        pen_menu = menubar.addMenu("Pen")
        pen_action = QAction("Pen", self)
        pen_action.triggered.connect(self.canvas.set_pen_tool)
        pen_color_action = QAction("Color", self)
        pen_color_action.triggered.connect(lambda: self.functions.select_color("pen"))
        set_size_action = QAction("Set size", self)
        set_size_action.triggered.connect(lambda: self.functions.set_size("pen"))
        pen_menu.addAction(set_size_action)
        pen_menu.addAction(pen_color_action)

        eraser_menu = menubar.addMenu("Eraser")
        eraser_action = QAction("Eraser", self)
        eraser_action.triggered.connect(self.canvas.set_eraser_tool)
        set_size_action_eraser = QAction("Set size", self)
        set_size_action_eraser.triggered.connect(lambda: self.functions.set_size("eraser"))
        eraser_menu.addAction(set_size_action_eraser)

        bucket_menu = menubar.addMenu("Bucket")
        bucket_action = QAction("Bucket", self)
        bucket_action.triggered.connect(self.canvas.set_bucket_tool)
        bucket_color_action = QAction("Color", self)
        bucket_color_action.triggered.connect(lambda: self.functions.select_color("bucket"))
        bucket_menu.addAction(bucket_color_action)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
