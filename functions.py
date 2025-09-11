from PyQt5.QtWidgets import QWidget, QColorDialog, QInputDialog, QFileDialog
from PyQt5.QtGui import QColor, QImage
from PIL import Image
from canvas import MyGraphicsView as canvas


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
        self.scene.fill(QColor("white"))
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

    def set_size(self, tool: str):
        if tool == "pen":
            current = self.canvas.pen_width
        elif tool == "eraser":
            current = self.canvas.eraser_width
        else:
            return
        size, ok = QInputDialog.getInt(self, "Set Size", f"Enter {tool} size:", value=current, min=1, max=50)
        if ok:
            if tool == "pen":
                self.canvas.pen_width = size
            elif tool == "eraser":
                self.canvas.eraser_width = size
