from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QWidget, QColorDialog, QInputDialog, QFileDialog, QFontDialog, QMainWindow
from PyQt5.QtGui import QColor, QImage, QPainter, QTransform
from PIL import Image
from resize_dialog import ResizeDialog


def pil2qimage(im: Image.Image):
    im = im.convert("RGBA")
    data = im.tobytes("raw", "RGBA")
    qimage = QImage(
        data,
        im.width,
        im.height,
        im.width * 4,
        QImage.Format_RGBA8888,
    )
    return qimage.copy()


class Functions(QWidget):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas

    def clear_canvas(self):
        self.canvas.scene.fill(QColor("white"))
        self.update()

    def save_canvas(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.canvas.scene.save(file_path)

    def load_canvas(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            im = Image.open(file_path)
            qimage = pil2qimage(im)
            self.canvas.scene = qimage
            self.canvas.setFixedSize(qimage.width(), qimage.height())
            self.canvas.update()

    def select_color(self, tool: str):
        color = QColorDialog.getColor(initial=self.canvas.pen_color, parent=self)
        if color.isValid():
            if tool == "pen":
                self.canvas.pen_color = color
            elif tool == "bucket":
                self.canvas.bucket_color = color
            elif tool == "selection":
                self.canvas.selection_fill_color = color
                return color
            elif tool == "text":
                self.canvas.text_color = color

    def set_size(self, tool: str):
        if tool == "pen":
            current = self.canvas.pen_width
        elif tool == "eraser":
            current = self.canvas.eraser_width
        else:
            return
        size, ok = QInputDialog.getInt(self, "Размер", f"Введите размер {tool}:", value=current, min=1, max=50)
        if ok:
            if tool == "pen":
                self.canvas.pen_width = size
            elif tool == "eraser":
                self.canvas.eraser_width = size

    def resize_canvas(self):
        current_w = self.canvas.width()
        current_h = self.canvas.height()
        dialog = ResizeDialog(current_w, current_h, self.canvas.parentWidget())
        if dialog.exec_():
            new_w, new_h = dialog.get_values()
            self.canvas.resize_canvas(new_w, new_h)
            main_window = self.canvas.window()
            menubar_height = main_window.menuBar().height() if isinstance(main_window, QMainWindow) else 0
            main_window.setFixedSize(new_w, new_h + menubar_height)

    def fill_selection(self):
        color = self.select_color("selection")
        if self.canvas.selection_rect is not None:
            rect = self.canvas.selection_rect.normalized()
            painter = QPainter(self.canvas.scene)
            painter.fillRect(rect, color)
            painter.end()
            self.canvas.update()

    def clear_selection(self):
        if self.canvas.selection_rect is not None:
            rect = self.canvas.selection_rect.normalized()
            painter = QPainter(self.canvas.scene)
            painter.fillRect(rect, QColor("white"))
            painter.end()
            self.canvas.update()

    def change_brightness(self, delta):
        if self.canvas.selection_rect and not self.canvas.selection_rect.isNull():
            rect = self.canvas.selection_rect.normalized()
        else:
            rect = self.canvas.scene.rect()
        for y in range(rect.top(), rect.bottom() + 1):
            for x in range(rect.left(), rect.right() + 1):
                old_color = QColor(self.canvas.scene.pixel(x, y))
                r, g, b = old_color.red(), old_color.green(), old_color.blue()
                new_r = max(0, min(255, r + delta))
                new_g = max(0, min(255, g + delta))
                new_b = max(0, min(255, b + delta))
                self.canvas.scene.setPixelColor(x, y, QColor(new_r, new_g, new_b))

        self.canvas.update()

    def make_blackwhite(self):
        if self.canvas.selection_rect and not self.canvas.selection_rect.isNull():
            rect = self.canvas.selection_rect.normalized()
        else:
            rect = self.canvas.scene.rect()
        for y in range(rect.top(), rect.bottom() + 1):
            for x in range(rect.left(), rect.right() + 1):
                old_color = QColor(self.canvas.scene.pixel(x, y))
                r, g, b = old_color.red(), old_color.green(), old_color.blue()
                gray = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
                self.canvas.scene.setPixelColor(x, y, QColor.fromRgbF(gray, gray, gray))

        self.canvas.update()

    def select_text_font(self):
        font, ok = QFontDialog.getFont(self.canvas.text_font, self, "Выберите шрифт")
        if not ok:
            return
        self.canvas.text_font = font

    def rotate_selection(self):
        if self.canvas.selection_rect is None:
            return

        if self.canvas.selection_image is None:
            self.canvas.selection_image = self.canvas.scene.copy(self.canvas.selection_rect)

        angle, ok = QInputDialog.getInt(
            self.canvas,
            "Угол поворота",
            "Введите значение (1 до 360):",
            min=1,
            max=360
        )
        if not ok:
            return

        self.canvas.rotate_angle = angle

        transform = QTransform().rotate(angle)
        rotated_image = self.canvas.selection_image.transformed(transform, Qt.SmoothTransformation)
        self.canvas.selection_image = rotated_image

        painter = QPainter(self.canvas.scene)
        painter.fillRect(self.canvas.selection_rect, QColor("white"))
        painter.drawImage(self.canvas.selection_rect.topLeft(), self.canvas.selection_image)
        painter.end()

        new_rect = QRect(self.canvas.selection_rect.topLeft(), rotated_image.size())
        self.canvas.selection_rect = new_rect
        self.canvas.update()

    def rotate_canvas(self):
        angle, ok = QInputDialog.getInt(
            self,
            "Угол поворота",
            "Введите значение (1 до 360):",
            min=1,
            max=360
        )
        if not ok:
            return
        self.canvas.rotate_angle = angle

        if not self.canvas.selection_rect or not self.canvas.selection_image:
            transform = QTransform().rotate(angle)
            rotated_scene = self.canvas.scene.transformed(transform, Qt.SmoothTransformation)
            self.canvas.scene = rotated_scene
            self.canvas.setFixedSize(self.canvas.scene.size())
            self.canvas.update()

    def flip_selection(self):
        if self.canvas.selection_rect is None:
            return
        if self.canvas.selection_image is None:
            self.canvas.selection_image = self.canvas.scene.copy(self.canvas.selection_rect)

        horizontal, ok = QInputDialog.getInt(
            self,
            "Отражение",
            "Введите значение (0 - по горизонтали, 1 - по вертикали):",
            min=0,
            max=1
        )
        if not ok:
            return

        transform = QTransform()
        if horizontal == 1:
            transform.scale(-1, 1)
        else:
            transform.scale(1, -1)

        flipped_image = self.canvas.selection_image.transformed(transform, Qt.SmoothTransformation)
        self.canvas.selection_image = flipped_image

        painter = QPainter(self.canvas.scene)
        painter.fillRect(self.canvas.selection_rect, QColor("white"))
        painter.drawImage(self.canvas.selection_rect.topLeft(), self.canvas.selection_image)
        painter.end()

        self.canvas.selection_rect = QRect(self.canvas.selection_rect.topLeft(), flipped_image.size())
        self.canvas.update()

    def flip_canvas(self):
        horizontal, ok = QInputDialog.getInt(
            self,
            "Отражение",
            "Введите значение (0 - по горизонтали, 1 - по вертикали):",
            min=0,
            max=1
        )
        if not ok:
            return
        self.canvas.is_horizontal_flip = horizontal

        if not self.canvas.selection_rect or not self.canvas.selection_image:
            transform = QTransform()
            if horizontal == 1:
                transform.scale(-1, 1)
            else:
                transform.scale(1, -1)
            flipped_scene = self.canvas.scene.transformed(transform, Qt.SmoothTransformation)
            self.canvas.scene = flipped_scene
            self.canvas.update()
