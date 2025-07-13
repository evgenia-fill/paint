from PyQt5.QtWidgets import QGraphicsView, QGraphicsPathItem
from PyQt5.QtGui import QPainterPath, QColor, QPen, QMouseEvent
from PyQt5.QtCore import Qt


class MyGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setMouseTracking(True)
        self.is_drawing = False
        self.path = QPainterPath()
        self.path_item = None
        self.color = QColor("black")
        self.width = 3
        self.tool = "pen"

    def set_tool(self, name):
        self.tool = name

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.is_drawing = True
            start_pos = self.mapToScene(event.pos())
            self.path = QPainterPath(start_pos)
            self.path_item = QGraphicsPathItem(self.path)
            if self.tool == "pen":
                pen = QPen(self.color, self.width)
            elif self.tool == "eraser":
                pen = QPen(QColor("white"), self.width * 1.5)
            self.path_item.setPen(pen)
            self.scene().addItem(self.path_item)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.is_drawing:
            current_pos = self.mapToScene(event.pos())
            self.path.lineTo(current_pos)
            self.path_item.setPath(self.path)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.is_drawing:
            self.is_drawing = False
