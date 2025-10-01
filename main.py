import os

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.abspath(
    ".venv/lib/python3.12/site-packages/PyQt5/Qt5/plugins/platforms")

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QPushButton, QVBoxLayout, QWidget, QInputDialog
from canvas import Canvas
from functions import Functions


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paint")
        self.resize(800, 600)
        self.canvas = Canvas(800, 600)
        self.setCentralWidget(self.canvas)
        self.functions = Functions(self.canvas)

        layout = QVBoxLayout()

        self.brightness_button = QPushButton("Изменить яркость")
        self.brightness_button.clicked.connect(self.open_brightness_dialog)
        self.grayscale_button = QPushButton("Сделать чб")
        self.grayscale_button.clicked.connect(self.functions.make_blackwhite)

        layout.addWidget(self.brightness_button)
        layout.addWidget(self.grayscale_button)
        layout.addWidget(self.canvas)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        menubar = self.menuBar()

        file_menu = menubar.addMenu("Файл")
        clear_action = QAction("Очистить все", self)
        clear_action.triggered.connect(self.functions.clear_canvas)
        save_action = QAction("Сохранить как", self)
        save_action.triggered.connect(self.functions.save_canvas)
        exit_action = QAction("Загрузить файл", self)
        exit_action.triggered.connect(self.functions.load_canvas)
        resize_action = QAction("Выбрать размер", self)
        resize_action.triggered.connect(self.functions.resize_canvas)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)
        file_menu.addAction(clear_action)
        file_menu.addAction(resize_action)

        canvas_menu = menubar.addMenu("Изображение")
        rotate_action = QAction("Повернуть на", self)
        rotate_action.triggered.connect(self.functions.rotate_canvas)
        flip_action = QAction("Отразить", self)
        flip_action.triggered.connect(self.functions.flip_canvas)
        canvas_menu.addAction(rotate_action)
        canvas_menu.addAction(flip_action)

        tools_menu = menubar.addMenu("Инструменты")
        tool_pen = QAction("Ручка", self)
        tool_pen.triggered.connect(self.canvas.set_pen_tool)
        tool_eraser = QAction("Ластик", self)
        tool_eraser.triggered.connect(self.canvas.set_eraser_tool)
        tool_bucket = QAction("Ведро", self)
        tool_bucket.triggered.connect(self.canvas.set_bucket_tool)
        tool_text = QAction("Текст", self)
        tool_text.triggered.connect(self.canvas.set_text_tool)
        tool_selection = QAction("Прямоугольное выделение", self)
        tool_selection.triggered.connect(self.canvas.set_selection_tool)
        tools_menu.addAction(tool_pen)
        tools_menu.addAction(tool_eraser)
        tools_menu.addAction(tool_bucket)
        tools_menu.addAction(tool_text)
        tools_menu.addAction(tool_selection)

        shapes_menu = menubar.addMenu("Геом фигуры")
        shapes_line = QAction("Линия", self)
        shapes_line.triggered.connect(self.canvas.set_line_tool)
        shapes_rect = QAction("Прямоугольник", self)
        shapes_rect.triggered.connect(self.canvas.set_rect_tool)
        shapes_ellipse = QAction("Круг", self)
        shapes_ellipse.triggered.connect(self.canvas.set_ellipse_tool)
        shapes_menu.addAction(shapes_line)
        shapes_menu.addAction(shapes_rect)
        shapes_menu.addAction(shapes_ellipse)

        pen_menu = menubar.addMenu("Ручка")
        pen_action = QAction("Pen", self)
        pen_action.triggered.connect(self.canvas.set_pen_tool)
        pen_color_action = QAction("Цвет", self)
        pen_color_action.triggered.connect(lambda: self.functions.select_color("pen"))
        set_size_action = QAction("Размер", self)
        set_size_action.triggered.connect(lambda: self.functions.set_size("pen"))
        pen_menu.addAction(set_size_action)
        pen_menu.addAction(pen_color_action)

        eraser_menu = menubar.addMenu("Ластик")
        eraser_action = QAction("Eraser", self)
        eraser_action.triggered.connect(self.canvas.set_eraser_tool)
        set_size_action_eraser = QAction("Размер", self)
        set_size_action_eraser.triggered.connect(lambda: self.functions.set_size("eraser"))
        eraser_menu.addAction(set_size_action_eraser)

        bucket_menu = menubar.addMenu("Ведро")
        bucket_action = QAction("Bucket", self)
        bucket_action.triggered.connect(self.canvas.set_bucket_tool)
        bucket_color_action = QAction("Цвет", self)
        bucket_color_action.triggered.connect(lambda: self.functions.select_color("bucket"))
        bucket_menu.addAction(bucket_color_action)

        selection_menu = menubar.addMenu("Выделение")
        selection_action = QAction("Selection", self)
        selection_action.triggered.connect(self.canvas.set_selection_tool)
        selection_color_action = QAction("Залить цветом", self)
        selection_color_action.triggered.connect(lambda: self.functions.fill_selection())
        selection_clear_action = QAction("Очистить все", self)
        selection_clear_action.triggered.connect(lambda: self.functions.clear_selection())
        selection_rotate_action = QAction("Повернуть на", self)
        selection_rotate_action.triggered.connect(self.functions.rotate_selection)
        selection_flip_action = QAction("Отразить", self)
        selection_flip_action.triggered.connect(self.functions.flip_selection)
        selection_menu.addAction(selection_color_action)
        selection_menu.addAction(selection_clear_action)
        selection_menu.addAction(selection_rotate_action)
        selection_menu.addAction(selection_flip_action)

        text_menu = menubar.addMenu("Текст")
        text_action = QAction("Text", self)
        text_action.triggered.connect(self.canvas.set_text_tool)
        text_color_action = QAction("Цвет", self)
        text_font_action = QAction("Шрифт", self)
        text_color_action.triggered.connect(lambda: self.functions.select_color("text"))
        text_font_action.triggered.connect(lambda: self.functions.select_text_font())
        text_menu.addAction(text_color_action)
        text_menu.addAction(text_font_action)

    def open_brightness_dialog(self):
        delta, ok = QInputDialog.getInt(
            self,
            "Регулировка яркости",
            "Введите значение (-255 до 255):",
            min=-255,
            max=255
        )
        if ok and delta != 0:
            self.functions.change_brightness(delta)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
