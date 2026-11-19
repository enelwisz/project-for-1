import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox
from PyQt6.QtGui import QPainter, QColor, QPen, QPixmap
from PyQt6.QtCore import Qt, QRect, QTimer

# ==============================================================================
# 1. КОНСТАНТЫ И СПИСКИ КАРТ (Данные уровней)
# ==============================================================================
GRAVEYARD_MAP = [
    "#########################################..",
    "#########################################..",
    "#........................................FF",
    "#.......G...#######...G..#######.######....",
    "#.......G...#.....#...G..#.......#.........",
    "#...........#.....#...G..#.......#.........",
    "####..#######..#..########..####.#..######.",
    "#..#..#........#............#....#..#....#.",
    "#..#..#........#............#.......#.GG.#.",
    "#..#..#.GG..#..######..######..#....#.####.",
    "#..####.GG..#.......#..#.GG....####........",
    "#.......GG..######..#....GG.......#........",
    "#................#..#.............#...GG.##",
    "#####...#####....#..###..########.#...GG.#.",
    "#...#...#....GG..#.......#......#.#......#.",
    "#...#...#....GG..#.......#..#...#.######.#.",
    "#...#####..####..#####...D..#...#........#.",
    "#..........#.....#...########...######...#.",
    "#..........#............#............#...#.",
    "#....GG....#.######.....#............#...#.",
    "#..S.GG......#....#..G..#######......#####.",
    "#........#####....#..G........#............",
    "##########........#..G....GG..#......W.....",
    "###########################################",
]

ROWS = len(GRAVEYARD_MAP)
COLS = len(GRAVEYARD_MAP[0])
TILE_SIZE = 25
OFFSET_X = 28
OFFSET_Y = 28


# ==============================================================================
# 2. КЛАСС ДЛЯ РАБОТЫ С БАЗОЙ ДАННЫХ (SQLite)
# ==============================================================================
class DatabaseManager:
    """Управление таблицей рекордов и сохранением результатов"""

    def __init__(self):
        # Тут будет инициализация sqlite3.connect('game_data.db')
        pass

    def init_database(self):
        """Создание таблиц рекордов, если их еще нет"""
        pass

    def save_record(self, player_name, level_name, time_spent, clicks):
        """Сохранение нового рекорда в базу данных"""
        pass

    def get_top_records(self, level_name):
        """Получение лучших результатов для таблицы рекордов"""
        return []


# ==============================================================================
# 3. КЛАСС АЛГОРИТМА ПОИСКА ПУТИ (Pathfinding)
# ==============================================================================
class Pathfinder:
    """Математический движок для расчета траекторий робота и Стража"""

    @staticmethod
    def find_path(grid, start, end):
        """Алгоритм BFS / A* для поиска кратчайшего пути по матрице"""
        # Возвращает список точек [(r,c), (r,c)...] в обход стен '#'
        return []


# ==============================================================================
# 4. КЛАССЫ ИГРОВЫХ СУЩНОСТЕЙ (Entities)
# ==============================================================================
class RobotAgent:
    """Главный герой — управляемый робот"""

    def __init__(self, start_row, start_col):
        self.row = start_row
        self.col = start_col
        self.x = 0  # Пиксельная координата X для плавной отрисовки
        self.y = 0  # Пиксельная координата Y
        self.path = []  # Список клеток текущего маршрута
        self.direction = "right"  # Для будущей смены 4 спрайтов

    def update_position(self):
        """Плавное перемещение по пикселям к следующей клетке из self.path"""
        pass


class PatrolBot:
    """Враг 1 и 2 — циклические патрульные боты"""

    def __init__(self, route_points):
        self.route = route_points  # Список точек, по которым бот ходит по кругу
        self.current_target_idx = 0
        self.x = 0
        self.y = 0

    def move(self):
        """Движение по фиксированному замкнутому маршруту"""
        pass


class GuardianBot:
    """Враг 3 — спящий Страж в тупике (Босс)"""

    def __init__(self, spawn_row, spawn_col):
        self.row = spawn_row
        self.col = spawn_col
        self.state = "SLEEP"  # Состояния: 'SLEEP' или 'HUNT'

    def activate_hunt(self, target_robot):
        """Переключение в режим погони и ежесекундный пересчет пути до Робота"""
        pass


# ==============================================================================
# 5. КЛАСС ИГРОВОГО ПОЛЯ (Визуализация и игровое ядро)
# ==============================================================================
class GameBoard(QWidget):
    """Кастомный виджет, где отрисовывается вся игра"""

    def __init__(self, image_path):
        super().__init__()
        self.setFixedSize(1200, 675)

        # Шаг 1: Загрузка картинки карты
        self.bg = QPixmap(image_path) if os.path.exists(image_path) else None

        # Шаг 2: Инициализация списка карты
        self.grid = [list(row) for row in GRAVEYARD_MAP]

        # Инициализация персонажей
        self.robot = RobotAgent(20, 3)
        self.patrols = []
        self.guardian = GuardianBot(22, 37)

        # Главный игровой таймер (60 FPS)
        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)

    def paintEvent(self, event):
        """Отрисовка фона-картинки, сетки, путей и спрайтов сущностей"""
        painter = QPainter(self)
        if self.bg:
            painter.drawPixmap(0, 0, self.width(), self.height(), self.bg)

        # Здесь будет QPainter рисовать кружочки робота, ботов и линию пути
        pass

    def mousePressEvent(self, event):
        """Событие клика: берем координаты и передаем в Pathfinder"""
        pass

    def game_loop(self):
        """Сердце игры: вызывается каждые 16мс, двигает всех и проверяет коллизии"""
        # 1. Сдвинуть робота
        # 2. Сдвинуть патрули
        # 3. Сдвинуть Стража (если HUNT)
        # 4. Проверить триггеры (наступил на G? наступил на F?)
        # 5. Проверить столкновение с ботами (Game Over)
        self.update()


# ==============================================================================
# 6. ГЛАВНОЕ ОКНО ПРИЛОЖЕНИЯ (Интерфейс и стили)
# ==============================================================================
class MainWindow(QMainWindow):
    """Окно с верхней панелью управления и встроенным дизайном QSS"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CyberRunner AI")

        # Создаем общую компоновку (Панель кнопок + Игровое поле)
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Верхняя панель (Интерфейс управления)
        self.top_panel = QWidget()
        self.panel_layout = QHBoxLayout(self.top_panel)

        # Заготовки под виджеты UI
        self.level_select = QComboBox()
        self.level_select.addItems(["1. Кладбище", "2. Джунгли (Скоро)", "3. Киберпанк (Скоро)"])
        self.btn_restart = QPushButton("Рестарт")
        self.btn_scores = QPushButton("Рекорды")
        self.lbl_timer = QLabel("Время: 0.0с")
        self.lbl_clicks = QLabel("Клики: 0")

        self.panel_layout.addWidget(self.level_select)
        self.panel_layout.addWidget(self.btn_restart)
        self.panel_layout.addWidget(self.btn_scores)
        self.panel_layout.addWidget(self.lbl_timer)
        self.panel_layout.addWidget(self.lbl_clicks)

        # Подключаем игровое поле
        self.board = GameBoard("assets/graveyard_1.png")

        self.main_layout.addWidget(self.top_panel)
        self.main_layout.addWidget(self.board)
        self.setCentralWidget(self.central_widget)

        self.apply_styles()

    def apply_styles(self):
        """Темная неоновая стилизация QSS для кнопок и панелей"""
        self.setStyleSheet("""
            QMainWindow { background-color: #0f1017; }
            QWidget#top_panel { background-color: #161822; border-bottom: 2px solid #232738; }
            QLabel { color: #8f9bb3; font-weight: bold; font-size: 14px; }
            QPushButton { background-color: #232738; color: white; border: 1px solid #3b4266; padding: 5px 15px; font-weight: bold; }
            QPushButton:hover { background-color: #3b4266; border-color: #00d2ff; }
        """)


# ==============================================================================
# ЗАПУСК ПРИЛОЖЕНИЯ
# ==============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())




