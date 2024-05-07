import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, \
    QWidget, QHBoxLayout, QLabel, QDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QPixmap
import sys

from logic.api_handler import api_handler
from logic.steam_parser import steam_parser
from logic.logging_handler import logger


def open_website():
    os.system("start https://projectrebirth.net")
    pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Project Rebirth Launcher")
        self.setGeometry(200, 200, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout(main_widget)

        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_widget)
        layout.addWidget(sidebar_widget)

        button1 = QPushButton("Open Main")
        button1.clicked.connect(lambda: logger.log(level="info", handler="window_handler", message="Button 1 clicked"))
        sidebar_layout.addWidget(button1)

        button_settings = QPushButton("Open Settings")
        button_settings.clicked.connect(self.open_settings_window)
        sidebar_layout.addWidget(button_settings)

        button_website = QPushButton("Open Website")
        button_website.clicked.connect(open_website)
        sidebar_layout.addWidget(button_website)

        main_section_widget = QWidget()
        main_section_layout = QVBoxLayout(main_section_widget)
        layout.addWidget(main_section_widget)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        main_section_layout.addWidget(self.table)

        self.populate_table()

    def populate_table(self):
        game_list = []
        logger.log(level="info", handler="window_handler", message=f"Getting games from API.")
        games = api_handler.get_games()
        for game_content in games["games"]:
            game_list.append({"name": game_content["name"], "image_url": game_content["image"],
                              "status": game_content["status"], "ID": game_content["id"]})

        for hidden_item in game_list:
            if hidden_item["status"] == "hidden":
                game_list.remove(hidden_item)
                logger.log(level="info", handler="window_handler", message=f"Removed hidden game: {hidden_item['ID']}")
        self.table.setRowCount(len(game_list))
        for i, item in enumerate(game_list):
            name_item = QTableWidgetItem(item["name"])
            self.table.setItem(i, 0, name_item)

            image_label = QLabel()
            pixmap = QPixmap()
            pixmap.loadFromData(api_handler.get_image(item["image_url"]).content)
            pixmap = pixmap.scaledToWidth(100)
            image_label.setPixmap(pixmap)
            self.table.setCellWidget(i, 1, image_label)

            # Add button in the third column that runs get_game for that game ID and opens a new window calles sub_view
            open_button = QPushButton("Open")
            # todo fix so this gets its OWN ID and not the last one added
            open_button.clicked.connect(lambda: self.show_subview(item["ID"]))
            self.table.setCellWidget(i, 2, open_button)
            #status_item = QTableWidgetItem(item["status"])
            #self.table.setItem(i, 2, status_item)

    def show_subview(self, game_id):
        sub_view = SubView(game_id)
        sub_view.show()


    def open_settings_window(self):
        settings_window = SettingsWindow()
        settings_window.exec_()


class SubView(QMainWindow):
    def __init__(self, game_id):
        super().__init__()
        logger.log(level="info", handler="window_handler", message=f"Opening subview for game: {game_id}")
        game_id = game_id
        # todo rework to not double request. Maybe cache images and or glob vals?
        games = api_handler.get_games()
        for game_content in games["games"]:
            if game_content["id"] == game_id:
                game_name = game_content["name"]
                image_url = game_content["image"]
                # game_image = api_handler.get_image(image_url).content
        game_info = api_handler.get_game(game_id).json()
        self.setWindowTitle(f"Game: {game_name}")
        self.setGeometry(200, 200, 800, 600)
        layout = QVBoxLayout()
        version_label = QLabel(f"Version: {game_info['version']}")
        layout.addWidget(version_label)
        team = QLabel(f"Team: {game_info['team']}")
        layout.addWidget(team)
        origin = QLabel(f"Origin: {game_info['origin']}")
        layout.addWidget(origin)
        official = QLabel(f"Official: {game_info['official']}")
        layout.addWidget(official)
        game_image_label = QLabel()
        pixmap = QPixmap()
        pixmap.loadFromData(api_handler.get_image(image_url).content)
        pixmap = pixmap.scaledToWidth(200)
        game_image_label.setPixmap(pixmap)
        layout.addWidget(game_image_label)

        game_name_label = QLabel(game_name)
        layout.addWidget(game_name_label)

        game_description_label = QLabel(game_info["description"])
        layout.addWidget(game_description_label)
        self.setLayout(layout)
        logger.log(level="info", handler="window_handler", message=f"Opened subview for game: {game_id}")


class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout()

        button1 = QPushButton("Button 1")
        layout.addWidget(button1)

        button2 = QPushButton("Button 2")
        layout.addWidget(button2)

        path_label = QLabel("Text input")
        layout.addWidget(path_label)

        self.path_input = QLineEdit()
        layout.addWidget(self.path_input)

        self.setLayout(layout)
