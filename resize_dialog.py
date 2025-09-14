from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

class ResizeDialog(QDialog):
    def __init__(self, current_w, current_h, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resize Canvas")

        self.width_input = QLineEdit(str(current_w))
        self.height_input = QLineEdit(str(current_h))

        layout = QVBoxLayout()
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Width:"))
        row1.addWidget(self.width_input)
        layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Height:"))
        row2.addWidget(self.height_input)
        layout.addLayout(row2)

        button_ok = QPushButton("Ok")
        button_ok.clicked.connect(self.accept)
        button_cancel = QPushButton("Cancel")
        button_cancel.clicked.connect(self.reject)

        row3 = QHBoxLayout()
        row3.addWidget(button_ok)
        row3.addWidget(button_cancel)
        layout.addLayout(row3)

        self.setLayout(layout)

    def get_values(self):
        return int(self.width_input.text()), int(self.height_input.text())
