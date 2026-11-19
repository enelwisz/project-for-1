import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QPixmap
from PyQt6.QtCore import Qt, QRect

COLS = 48
ROWS = 27
TILE_SIZE = 25  # Итоговое окно 1200 x 675


class MapEditor(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.setFixedSize(COLS * TILE_SIZE, ROWS * TILE_SIZE)
        self.setMouseTracking(True)
        self.hover = (0, 0)
        self.brush = None

        self.bg = QPixmap(image_path) if os.path.exists(image_path) else None
        if not self.bg or self.bg.isNull():
            print(f"ВНИМАНИЕ: Файл не найден по пути {image_path}")

        # Начальная рамка из стен
        self.grid = [
            ["#" if r in (0, ROWS - 1) or c in (0, COLS - 1) else "." for c in range(COLS)]
            for r in range(ROWS)
        ]

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.bg and not self.bg.isNull():
            painter.drawPixmap(0, 0, self.width(), self.height(), self.bg)

        for r in range(ROWS):
            for c in range(COLS):
                rect = QRect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                painter.setPen(QPen(QColor(255, 255, 255, 45), 1))
                painter.drawRect(rect)

                cell = self.grid[r][c]
                if cell == "#":
                    painter.fillRect(rect, QColor(255, 40, 40, 120))
                elif cell == "G":
                    painter.fillRect(rect, QColor(180, 0, 255, 145))
                elif cell == "D":
                    painter.fillRect(rect, QColor(255, 220, 0, 145))
                elif cell == "S":
                    painter.setBrush(QColor(0, 210, 255, 240))
                    painter.drawEllipse(rect.adjusted(3, 3, -3, -3))
                elif cell == "F":
                    painter.setBrush(QColor(0, 255, 120, 240))
                    painter.drawEllipse(rect.adjusted(3, 3, -3, -3))
                elif cell == "W":
                    painter.setBrush(QColor(255, 120, 0, 240))
                    painter.drawEllipse(rect.adjusted(3, 3, -3, -3))

    def paint_cell(self, r, c):
        if 0 <= r < ROWS and 0 <= c < COLS and self.brush:
            self.grid[r][c] = self.brush
            self.update()

    def mousePressEvent(self, event):
        c = int(event.position().x()) // TILE_SIZE
        r = int(event.position().y()) // TILE_SIZE
        if not (0 <= r < ROWS and 0 <= c < COLS):
            return

        if event.button() == Qt.MouseButton.LeftButton:
            self.brush = "." if (event.modifiers() & Qt.KeyboardModifier.ShiftModifier) else "#"
        elif event.button() == Qt.MouseButton.RightButton:
            self.brush = "." if self.grid[r][c] == "G" else "G"

        self.paint_cell(r, c)

    def mouseMoveEvent(self, event):
        c = int(event.position().x()) // TILE_SIZE
        r = int(event.position().y()) // TILE_SIZE
        if 0 <= r < ROWS and 0 <= c < COLS:
            self.hover = (r, c)
            if self.brush:
                self.paint_cell(r, c)

    def mouseReleaseEvent(self, event):
        self.brush = None

    def keyPressEvent(self, event):
        r, c = self.hover
        key = event.key()
        if key == Qt.Key.Key_S:
            self.grid[r][c] = "S"
        elif key == Qt.Key.Key_F:
            self.grid[r][c] = "F"
        elif key == Qt.Key.Key_W:
            self.grid[r][c] = "W"
        elif key == Qt.Key.Key_D:
            self.grid[r][c] = "D"
        elif key == Qt.Key.Key_Space:
            print("\nGRAVEYARD_MAP = [")
            for row in self.grid:
                print(f'    "{"".join(row)}",')
            print("]\n")
        self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Разметчик новой карты")
        # Указываем путь к НОВОМУ файлу
        self.editor = MapEditor("assets/graveyard_1.png")
        self.editor.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setCentralWidget(self.editor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

