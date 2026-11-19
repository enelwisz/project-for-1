import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CyberRunner AI")
        self.setFixedSize(1080, 630)  # Формат 16:9 под твою карту
        self.setStyleSheet("background-color: #161822;")

        # Создаем виджет для вывода картинки
        self.bg_label = QLabel(self)
        self.bg_label.setFixedSize(1080, 630)

        image_path = "assets/graveyard.png"
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            # Масштабируем картинку ровно под размер окна
            self.bg_label.setPixmap(
                pixmap.scaled(
                    1080,
                    630,
                    Qt.AspectRatioMode.IgnoreAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            print(f"Картинка не найдена по пути: {image_path}")

        self.setCentralWidget(self.bg_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
