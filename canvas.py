from PyQt5.QtWidgets import QWidget, QInputDialog
from PyQt5.QtGui import QColor, QPen, QMouseEvent, QImage, QPainter, QFont
from PyQt5.QtCore import Qt, QPoint, QRect
from functions import Functions


class Canvas(QWidget):
    def __init__(self, weight=600, height=800):
        super().__init__()
        self.start_point = None
        self.last_point = None
        self.scene = QImage(weight, height, QImage.Format_ARGB32)
        self.scene.fill(QColor("white"))
        self.pen_width = 3
        self.eraser_width = 4
        self.pen_color = QColor("black")
        self.bucket_color = QColor("blue")
        self.text_color = QColor("black")
        self.text_font = QFont("Arial", 12)
        self.tool = "pen"  # pen, eraser, bucket, shapes, selection, text
        self.setFixedSize(weight, height)
        self.selection_rect = None
        self.selection_image = None
        self.selection_is_active = False
        self.selection_is_moving = False
        self.selection_fill_color = QColor("red")
        self.start_move = None
        self.move_offset = QPoint(0, 0)
        self.functions = Functions(self)
        self.rotate_angle = None
        self.is_horizontal_flip = None
        self.delta = None

    def set_tool(self, name):
        self.tool = name

    def set_pen_tool(self):
        self.tool = "pen"

    def set_eraser_tool(self):
        self.tool = "eraser"

    def set_bucket_tool(self):
        self.tool = "bucket"

    def set_line_tool(self):
        self.tool = "line"

    def set_rect_tool(self):
        self.tool = "rect"

    def set_ellipse_tool(self):
        self.tool = "ellipse"

    def set_selection_tool(self):
        self.tool = "selection"

    def set_text_tool(self):
        self.tool = "text"

    def set_text_font(self, font):
        self.text_font = font

    def set_pen_width(self, width):
        self.pen_width = width

    def set_pen_color(self, color):
        self.pen_color = color

    def set_bucket_color(self, color):
        self.bucket_color = color

    def set_text_color(self, color):
        self.text_color = color

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.scene)

        if self.selection_rect and not self.selection_rect.isNull():
            if self.selection_is_moving and self.selection_image is not None:
                painter.drawImage(self.selection_rect.topLeft(), self.selection_image)

            pen = QPen(Qt.blue, 1, Qt.DashLine)
            painter.setPen(pen)
            painter.drawRect(self.selection_rect)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            start_pos = event.pos()

            if self.tool == "bucket":
                if self.selection_rect and self.selection_rect.contains(event.pos()):
                    self.fill_selection()
                else:
                    self.fill_bucket(start_pos.x(), start_pos.y(), self.bucket_color)
                self.update()

            elif self.tool == "pen":
                self.last_point = start_pos
                self.draw_line(start_pos)

            elif self.tool == "eraser":
                if self.selection_rect and self.selection_rect.contains(event.pos()):
                    self.clear_selection()
                else:
                    self.last_point = start_pos
                self.draw_line(start_pos)

            elif self.tool == "text":
                self.add_text(start_pos)
                self.update()

            elif self.tool in ["line", "rect", "ellipse"]:
                self.start_point = start_pos

            elif self.tool == "selection":
                if self.selection_rect and self.selection_rect.contains(event.pos()):
                    self.selection_is_moving = True
                    self.start_move = event.pos()
                    if self.selection_image is None:
                        self.selection_image = self.scene.copy(self.selection_rect)
                        painter = QPainter(self.scene)
                        painter.fillRect(self.selection_rect, QColor("white"))
                        painter.end()
                else:
                    self.selection_is_moving = False
                    self.start_point = event.pos()
                    self.selection_rect = QRect()
                    self.selection_image = None

    def mouseMoveEvent(self, event: QMouseEvent):
        pos = event.pos()
        if self.tool in ["eraser", "pen"] and self.last_point is not None:
            self.draw_line(event.pos())

        elif self.tool == "selection":
            if self.selection_is_moving and self.selection_rect:
                dx = pos.x() - self.start_move.x()
                dy = pos.y() - self.start_move.y()
                self.selection_rect.translate(dx, dy)
                self.start_move = pos
                self.update()
            elif self.start_point:
                self.selection_rect = QRect(self.start_point, pos).normalized()
                self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.tool in ["line", "rect", "ellipse"] and self.start_point is not None:
            end_point = event.pos()
            painter = QPainter(self.scene)
            pen = QPen(self.pen_color, self.pen_width)
            painter.setPen(pen)
            if self.tool == "line":
                painter.drawLine(self.start_point, end_point)
            elif self.tool == "rect":
                rect = QRect(self.start_point, end_point)
                painter.drawRect(rect)
            elif self.tool == "ellipse":
                rect = QRect(self.start_point, end_point)
                painter.drawEllipse(rect)

            self.start_point = None
            self.update()

        elif self.tool == "selection" and event.button() == Qt.LeftButton:
            if self.selection_is_moving:
                if self.selection_image is not None:
                    painter = QPainter(self.scene)
                    painter.drawImage(self.selection_rect.topLeft(), self.selection_image)
                    painter.end()
                self.selection_is_moving = False
                self.selection_image = None
                self.start_move = None
            else:
                self.start_point = None

            self.update()

        elif self.tool in ["pen", "eraser"]:
            self.last_point = None

    def draw_line(self, end_pos):
        painter = QPainter(self.scene)

        if self.tool == "pen":
            pen = QPen(self.pen_color, self.pen_width)

        elif self.tool == "eraser":
            pen = QPen(QColor("white"), self.eraser_width)

        painter.setPen(pen)
        painter.drawLine(self.last_point, end_pos)
        self.last_point = end_pos
        self.update()

    def fill_bucket(self, x, y, new_color):
        target_color = QColor(self.scene.pixel(x, y))
        if target_color == new_color:
            return
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if 0 <= cx < self.scene.width() and 0 <= cy < self.scene.height():
                current_color = QColor(self.scene.pixel(cx, cy))
                if current_color == target_color:
                    self.scene.setPixelColor(cx, cy, new_color)
                    stack.extend([(cx + dx, cy + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]])

    def resize_canvas(self, w, h):
        new_scene = QImage(w, h, QImage.Format_RGB16)
        new_scene.fill(Qt.white)
        painter = QPainter(new_scene)
        painter.drawImage(0, 0, self.scene)
        painter.end()
        self.scene = new_scene
        self.setFixedSize(w, h)
        self.update()

    def add_text(self, pos):
        text, ok = QInputDialog.getText(self, "Ввод текста", "Введите текст:")
        if not ok or not text:
            return

        painter = QPainter(self.scene)
        painter.setFont(self.text_font)
        painter.setPen(QPen(self.text_color))
        painter.drawText(pos.x(), pos.y(), text)
        painter.end()
