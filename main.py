# ==============================================================================
# 1. ИМПОРТЫ
# ==============================================================================
import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt, QTimer



GRID_CONFIG = {
    "tile_size": 25,
    "offset_x": 28,
    "offset_y": 28
}

# ==============================================================================
# 2. БАЗА ДАННЫХ И СКЛ
# ==============================================================================
class DatabaseManager:
    """Управление локальной БД SQLite"""

    def __init__(self):
        pass


# ==============================================================================
# 3. КЛАСС ПОИСКА ПУТИ
# ==============================================================================
class Pathfinder:
    """Алгоритм поиска кратчайшего пути"""
    pass


# ==============================================================================
# 4. КЛАСС ОТЕЦ ДЛЯ ВСЕГО ЖИВОГО
# ==============================================================================
class BaseEntity:
    """Абстрактный родитель для персонажей"""
    pass


# ==============================================================================
# 5. КЛАСС БОТОВ
# ==============================================================================
class PatrolBot(BaseEntity):
    """Патрульный бот"""
    pass


# ==============================================================================
# 6. КЛАСС РОБОТА
# ==============================================================================
class RobotPlayer(BaseEntity):
    """Робот под управлением игрока"""
    pass


# ==============================================================================
# 7. КЛАСС БОССА
# ==============================================================================
class GuardianBoss(BaseEntity):
    """Спящий страж-босс"""
    pass


# ==============================================================================
# 8. КЛАСС КАРТЫ ГДЕ ВСЕ ЗАГРУЖАЕТСЯ
# ==============================================================================
class GameMapWidget(QWidget):
    """Экран игры: загрузка картинки, распаковка JSON и обработка кликов"""

    def __init__(self, image_path, json_path):
        super().__init__()
        self.setFixedSize(1200, 675)

        # 1. Загрузка картинки карты
        self.bg_pixmap = QPixmap(image_path) if os.path.exists(image_path) else None

        # 2. Распаковка матрицы из JSON
        self.matrix = []
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                self.matrix = [list(row) for row in raw_data["graveyard"]]

        self.rows = len(self.matrix)
        self.cols = len(self.matrix) if self.rows > 0 else 0

        # СЮДА ВСТАВЛЯЕМ ТОЛЬКО ПЕРЕМЕННЫЕ ПАМЯТИ (в самый конец __init__)
        self.saved_row = None
        self.saved_col = None

    def paintEvent(self, event):
        """Отрисовка заднего фона"""
        painter = QPainter(self)
        if self.bg_pixmap:
            painter.drawPixmap(0, 0, self.width(), self.height(), self.bg_pixmap)

    # А СЮДА (ниже paintEvent) ВСТАВЛЯЕМ ОБРАБОТКУ КЛИКОВ КАК ОТДЕЛЬНЫЙ МЕТОД
    def mousePressEvent(self, event):
        """ОБРАБОТКА КЛИКОВ: Перевод пикселей экрана в координаты ячейки матрицы"""
        if event.button() == Qt.MouseButton.LeftButton:

            # Математика: вычитаем отступ и делим на размер клетки
            col = (int(event.position().x()) - GRID_CONFIG["offset_x"]) // GRID_CONFIG["tile_size"]
            row = (int(event.position().y()) - GRID_CONFIG["offset_y"]) // GRID_CONFIG["tile_size"]

            # Проверяем границы сетки лабиринта
            if 0 <= row < self.rows and 0 <= col < self.cols:
                # Перезаписываем глобальную память, созданную в __init__
                self.saved_row = row
                self.saved_col = col

                cell_type = self.matrix[self.saved_row][self.saved_col]
                print(f"Данные сохранены! Цель: [{self.saved_row}][{self.saved_col}] | Тип: '{cell_type}'")
            else:
                print("Клик мимо игровой зоны!")

    def paintEvent(self, event):
        """Отрисовка заднего фона"""
        painter = QPainter(self)
        if self.bg_pixmap:
            painter.drawPixmap(0, 0, self.width(), self.height(), self.bg_pixmap)


# ==============================================================================
# 9. КЛАСС ГЛАВНОГО ОКНА
# ==============================================================================
class MainWindow(QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CyberRunner AI")

        # Подключаем виджет карты
        self.game_surface = GameMapWidget("assets/graveyard_1.png", "maps.json")
        self.setCentralWidget(self.game_surface)


# ==============================================================================
# 10. ЗАПУСК ПРИЛОЖЕНИЯ
# ==============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())





