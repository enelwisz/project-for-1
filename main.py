# ==============================================================================
# 1. ИМПОРТЫ
# ==============================================================================
import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QGuiApplication
import heapq




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
    """Умный движок поиска пути на базе алгоритма A* (A-Star)"""

    @staticmethod
    def get_path(matrix, start, goal):
        """Возвращает кратчайший путь от старта до цели в обход стен '#' и 'D'"""
        # Если старт и финиш совпадают — ехать никуда не надо
        if start == goal:
            return []

        # Динамически определяем реальные размеры нашей JSON-карты
        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0

        # Очередь приоритетов (F, клетка)
        open_set = []

        # Журнал стоимости шагов (G)
        G = {start: 0}

        # Словарь предков для восстановления маршрута
        parent = {}

        # Считаем эвристику (H) Манхэттенского расстояния до цели
        start_h = abs(start[0] - goal[0]) + abs(start[1] - goal[1])
        heapq.heappush(open_set, (start_h, start))

        while open_set:
            current_f, current = heapq.heappop(open_set)

            # Если дошли до цели — собираем путь назад по родительским стрелкам
            if current == goal:
                path = []
                while current in parent:
                    path.append(current)
                    current = parent[current]
                # Возвращаем путь, развернув его от старта к финишу
                # Отрезаем саму стартовую клетку (path[::-1][1:]), чтобы робот не дергался на месте
                return path[::-1]

            r, c = current
            # Проверяем 4 направления вокруг
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (r + dr, c + dc)
                nr, nc = neighbor

                # 1. Проверка динамических границ нашей карты
                if 0 <= nr < rows and 0 <= nc < cols:
                    # 2. Проверка препятствий: '#' (стена) и 'D' (закрытая дверь склепа) — непроходимы
                    if matrix[nr][nc] in ("#", "D"):
                        continue

                    new_g = G[current] + 1

                    if new_g < G.get(neighbor, float("inf")):
                        parent[neighbor] = current
                        G[neighbor] = new_g

                        h = abs(nr - goal[0]) + abs(nc - goal[1])
                        f = new_g + h

                        heapq.heappush(open_set, (f, neighbor))

        return []  # Безопасно возвращаем пустой список, если прохода нет


# ==============================================================================
# 4. КЛАСС ОТЕЦ ДЛЯ ВСЕГО ЖИВОГО
# ==============================================================================
class BaseEntity:
    """Абстрактный родитель для всех персонажей игры (Робот, Боты, Босс)"""

    def __init__(self, r, c, color_hex, speed=3):
        self.row = r  # Текущая строка в матрице
        self.col = c  # Текущий столбец в матрице
        self.color = QColor(color_hex)
        self.speed = speed

        # Переводим клетку матрицы в точные пиксели центра этой клетки на экране
        # Формула: Отступ + (Номер клетки * Размер) + Половина клетки (чтобы встать ровно по центру)
        self.x = GRID_CONFIG["offset_x"] + c * GRID_CONFIG["tile_size"] + GRID_CONFIG["tile_size"] // 2
        self.y = GRID_CONFIG["offset_y"] + r * GRID_CONFIG["tile_size"] + GRID_CONFIG["tile_size"] // 2

    def draw(self, painter):
        """Общий метод отрисовки примитива (круга) для всех существ"""
        painter.setBrush(self.color)
        painter.setPen(QPen(Qt.GlobalColor.white, 1))  # Белая тонкая обводка
        radius = 9  # Радиус круга (чуть меньше клетки 25x25)

        # Рисуем круг по текущим пиксельным координатам
        painter.drawEllipse(int(self.x - radius), int(self.y - radius), radius * 2, radius * 2)


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
    """Робот под управлением игрока (Наследует всё от BaseEntity)"""
    def __init__(self, r, c):
        super().__init__(r, c, color_hex="#00d2ff", speed=3) # Скорость 3 пикселя за кадр
        self.path = [] # Список клеток маршрута, полученный от A*

    def move_along_path(self):
        """Плавное попиксельное движение робота по точкам из self.path"""
        if not self.path:
            return  # Если пути нет — стоим на месте

        # Берем самую первую клетку из маршрута как текущую цель
        target_row, target_col = self.path[0]

        # Рассчитываем точные пиксельные координаты центра этой целевой клетки
        target_x = GRID_CONFIG["offset_x"] + target_col * GRID_CONFIG["tile_size"] + GRID_CONFIG["tile_size"] // 2
        target_y = GRID_CONFIG["offset_y"] + target_row * GRID_CONFIG["tile_size"] + GRID_CONFIG["tile_size"] // 2

        # Плавно двигаем координату X к цели
        if self.x < target_x:
            self.x = min(self.x + self.speed, target_x)
        elif self.x > target_x:
            self.x = max(self.x - self.speed, target_x)

        # Плавно двигаем координату Y к цели
        if self.y < target_y:
            self.y = min(self.y + self.speed, target_y)
        elif self.y > target_y:
            self.y = max(self.y - self.speed, target_y)

        # Если робот физически доехал пикселями до центра этой клетки
        if self.x == target_x and self.y == target_y:
            # Обновляем его текущее логическое положение в матрице
            self.row = target_row
            self.col = target_col
            # Удаляем эту клетку из маршрута, чтобы на следующем кадре ехать к следующей
            self.path.pop(0)



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
    """Экран игры: загрузка картинки, распаковка JSON, игровой цикл и клики мыши"""

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

        # Динамически запоминаем размеры сетки из загруженного JSON
        self.rows = len(self.matrix)
        self.cols = len(self.matrix) if self.rows > 0 else 0

        # Переменные для сохранения последней выбранной цели клика
        self.saved_row = None
        self.saved_col = None

        # Спавним робота на стартовую позицию (строка 20, колонка 3 — там где буква 'S')
        self.robot = RobotPlayer(20, 3)

    def paintEvent(self, event):
        """Отрисовка заднего фона и персонажей поверх него"""
        painter = QPainter(self)
        if self.bg_pixmap:
            painter.drawPixmap(0, 0, self.width(), self.height(), self.bg_pixmap)

        # Даем команду роботу нарисовать себя поверх карты
        self.robot.draw(painter)

    def mousePressEvent(self, event):
        """ОБРАБОТКА КЛИКОВ: Перевод пикселей экрана в ячейку матрицы и запуск A*"""
        if event.button() == Qt.MouseButton.LeftButton:

            # Математика: вычитаем отступ и делим на размер клетки
            col = (int(event.position().x()) - GRID_CONFIG["offset_x"]) // GRID_CONFIG["tile_size"]
            row = (int(event.position().y()) - GRID_CONFIG["offset_y"]) // GRID_CONFIG["tile_size"]

            # Проверяем, что клик не вылетел за границы игровой сетки лабиринта
            if 0 <= row < self.rows and 0 <= col < self.cols:
                # Нам строго запрещено кликать в стены '#' или закрытые двери 'D'
                if self.matrix[row][col] not in ("#", "D"):
                    # Сохраняем координаты цели в память виджета
                    self.saved_row = row
                    self.saved_col = col

                    # Запрашиваем маршрут у твоего класса Pathfinder с алгоритмом A*:
                    # Передаем: матрицу, текущую позицию робота и сохраненные координаты клика
                    calculated_path = Pathfinder.get_path(
                        self.matrix,
                        (self.robot.row, self.robot.col),
                        (self.saved_row, self.saved_col)
                    )

                    # Записываем посчитанный список клеток прямо в карман нашему роботу
                    self.robot.path = calculated_path

                    print(f"Путь рассчитан алгоритмом A*! Длина маршрута: {len(calculated_path)} шагов.")
            else:
                print("Клик за пределами лабиринта!")


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

    def showEvent(self, event):
        super().showEvent(event)
        # Этот код сработает ОДИН РАЗ в момент, когда окно РЕАЛЬНО появилось и приняло финальный размер
        window_geometry = self.frameGeometry()
        from PyQt6.QtGui import QCursor
        screen = QGuiApplication.screenAt(QCursor.pos())
        if not screen:
            screen = QGuiApplication.primaryScreen()

        screen_center = screen.geometry().center()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft())


# ==============================================================================
# 10. ЗАПУСК ПРИЛОЖЕНИЯ
# ==============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())





