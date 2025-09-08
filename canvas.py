from PyQt5.QtWidgets import QWidget, QColorDialog, QInputDialog
from PyQt5.QtGui import QColor, QPen, QMouseEvent, QImage, QPainter
from PyQt5.QtCore import Qt


class MyGraphicsView(QWidget):
    def __init__(self, weight=600, height=800):
        super().__init__()
        self.last_point = None
        self.scene = QImage(weight, height, QImage.Format_RGB16)
        self.scene.fill(QColor("white"))
        self.pen_width = 3
        self.eraser_width = 4
        self.pen_color = QColor("black")
        self.bucket_color = QColor("blue")
        self.tool = "pen"  # pen, eraser, bucket
        self.setFixedSize(weight, height)

    def set_tool(self, name):
        self.tool = name

    def set_pen_tool(self):
        self.tool = "pen"

    def set_eraser_tool(self):
        self.tool = "eraser"

    def set_bucket_tool(self):
        self.tool = "bucket"

    def set_pen_width(self, width):
        self.pen_width = width

    def set_pen_color(self, color):
        self.pen_color = color

    def set_bucket_color(self, color):
        self.bucket_color = color

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.scene)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            start_pos = event.pos()
            if self.tool == "bucket":
                self.fill_bucket(start_pos.x(), start_pos.y(), self.bucket_color)
                self.update()
            else:
                self.last_point = start_pos
                self.draw_line(start_pos)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.tool in ["eraser", "pen"] and self.last_point is not None:
            self.draw_line(event.pos())

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.tool in ["eraser", "pen"] and self.last_point is not None:
            self.draw_line(event.pos())
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

    def clear_canvas(self):
        pass

    def save_canvas(self):
        pass

    def exit_canvas(self):
        pass

    def select_color(self, tool: str):
        color = QColorDialog.getColor(initial=self.pen_color, parent=self)
        if color.isValid():
            if tool == "pen":
                self.pen_color = color
            elif tool == "bucket":
                self.bucket_color = color

    def set_size(self, tool: str):
        if tool == "pen":
            current = self.pen_width
        elif tool == "eraser":
            current = self.eraser_width
        else:
            return
        size, ok = QInputDialog.getInt(self, "Set Size", f"Enter {tool} size:", value=current, min=1, max=50)
        if ok:
            if tool == "pen":
                self.pen_width = size
            elif tool == "eraser":
                self.eraser_width = size
