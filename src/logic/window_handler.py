import os

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, \
    QWidget, QHBoxLayout, QLabel, QDialog, QLineEdit, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from logic.api_handler import api_handler
from logic.steam_parser import steam_parser
from logic.logging_handler import logger
from logic.file_handler import file_handler
from logic.setup_handlers import update_config_item, load_config


def open_website():
    os.system("start https://projectrebirth.net")
    pass


def show_subview(game_id):
    sub_view = SubView(game_id)
    sub_view.exec_()


def open_settings_window():
    settings_window = SettingsWindow()
    settings_window.exec_()


def get_health():
    logger.log(level="info", handler="window_handler", message="Checking API health.")
    health = api_handler.get_healthcheck()
    if health.json()["Health"] == "Alive":
        return "Online"
    else:
        return "Error"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Project Rebirth Launcher")
        # 1400x700
        self.setGeometry(200, 200, 1400, 700)
        self.setStyleSheet("background-color: #333333; color: white;")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout(main_widget)

        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_widget)
        layout.addWidget(sidebar_widget)

        button1 = QPushButton("Open Main")
        button1.setStyleSheet("background-color: #6A5ACD; color: white;")
        button1.clicked.connect(lambda: logger.log(level="info", handler="window_handler", message="Button 1 clicked"))
        sidebar_layout.addWidget(button1)

        button_settings = QPushButton("Open Settings")
        button_settings.setStyleSheet("background-color: #6A5ACD; color: white;")
        button_settings.clicked.connect(open_settings_window)
        sidebar_layout.addWidget(button_settings)

        button_website = QPushButton("Open Website")
        button_website.setStyleSheet("background-color: #6A5ACD; color: white;")
        button_website.clicked.connect(open_website)
        sidebar_layout.addWidget(button_website)

        # Todo update this every few seconds to see if the API is still online
        api_status_label = QLabel()
        api_status_label.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        api_status_label.setText("API Status: " + get_health())

        sidebar_layout.addWidget(api_status_label)

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
        self.table.setStyleSheet("background-color: #333333; color: white;")
        num = 0
        for i, item in enumerate(game_list):
            name_item = QTableWidgetItem(item["name"])
            self.table.setItem(i, 0, name_item)
            image_label = QLabel()
            pixmap = QPixmap()
            pixmap.loadFromData(api_handler.get_image(item["image_url"]).content)
            pixmap = pixmap.scaledToWidth(300)
            pixmap = pixmap.scaledToHeight(450)
            self.table.setRowHeight(num, 450)
            image_label.setPixmap(pixmap)
            self.table.setCellWidget(i, 1, image_label)
            open_button = QPushButton("Open")
            open_button.setStyleSheet("background-color: #6A5ACD; color: white;")
            open_button.clicked.connect(lambda checked, item_id=item["ID"]: show_subview(item_id))
            self.table.setCellWidget(i, 2, open_button)
            num += 1
        self.table.setColumnWidth(1, 300)


class SubView(QDialog):
    def __init__(self, game_id):
        super().__init__()

        logger.log(level="debug", handler="window_handler", message=f"Opening subview for game: {game_id}")

        games = api_handler.get_games()
        for game_content in games["games"]:
            if game_content["id"] == game_id:
                game_name = game_content["name"]
                image_url = game_content["image"]
                game_info = api_handler.get_game(game_id).json()
                break

        self.setWindowTitle(f"Game: {game_name}")
        self.setGeometry(200, 200, 800, 600)
        layout = QGridLayout()
        self.setStyleSheet("background-color: #333333; color: white;")

        game_image_label = QLabel()
        pixmap = QPixmap()
        pixmap.loadFromData(api_handler.get_image(image_url).content)
        pixmap = pixmap.scaledToWidth(200)
        game_image_label.setPixmap(pixmap)
        layout.addWidget(game_image_label, 0, 0, 3, 1)

        game_name_label = QLabel(game_name)
        layout.addWidget(game_name_label, 3, 0, 1, 1)

        download_button = QPushButton("Download Game")
        download_button.setStyleSheet("background-color: #6A5ACD; color: white;")
        # todo THIS DOES NO EXIST YET
        # Needs to be added on the API
        # download_button.clicked.connect(lambda: file_handler.download_base_game(game_id))
        layout.addWidget(download_button, 4, 0, 1, 1)

        path_button = QPushButton("Patch Game")
        path_button.setStyleSheet("background-color: #6A5ACD; color: white;")
        path_button.clicked.connect(lambda: self.patch_game(game_id))
        layout.addWidget(path_button, 5, 0, 1, 1)

        version_label = QLabel(f"Version: {game_info['version']}")
        layout.addWidget(version_label, 0, 1, 1, 1)

        team_label = QLabel(f"Team: {game_info['team']} (behind the rebirth)")
        layout.addWidget(team_label, 1, 1, 1, 1)

        official_label = QLabel("Official: " + ("Yes" if game_info['official'] else "No"))
        layout.addWidget(official_label, 2, 1, 1, 1)

        game_description_label = QLabel(game_info["description"])
        layout.addWidget(game_description_label, 3, 1, 2, 1)

        self.setLayout(layout)
        logger.log(level="debug", handler="window_handler", message=f"Opened subview for game: {game_id}")

    def patch_game(self, game_id):
        data = api_handler.get_patch(game_id).json()
        return_val = file_handler.patcher(data)
        if return_val:
            logger.log(level="info", handler="window_handler", message=f"Patched game: {game_id}")
            message_box("Success", "Game patched successfully").exec_()
        else:
            logger.log(level="error", handler="window_handler", message=f"Failed to patch game: {game_id}")
            message_box("Error", "Failed to patch game").exec_()


def patch():
    ret_val = steam_parser.parse()
    if ret_val:
        message_box("Success", "Steam library scanned successfully").exec_()
    else:
        message_box("Error", "Failed to scan steam library").exec_()


class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        logger.log(level="debug", handler="window_handler", message="Opening settings window")
        self.setWindowTitle("Settings")
        self.setGeometry(300, 300, 300, 200)
        self.setStyleSheet("background-color: #333333; color: white;")
        config = load_config()

        layout = QVBoxLayout()
        steam_scan = QPushButton("Rescan Steam Library")
        steam_scan.setStyleSheet("background-color: #6A5ACD; color: white;")
        steam_scan.clicked.connect(lambda: patch())
        layout.addWidget(steam_scan)
        button_report_bug = QPushButton("Report a Bug")
        button_report_bug.setStyleSheet("background-color: #6A5ACD; color: white;")
        # todo add logic to open a bug report form
        layout.addWidget(button_report_bug)
        button_request_feature = QPushButton("Request a Feature")
        button_request_feature.setStyleSheet("background-color: #6A5ACD; color: white;")
        # todo add logic to open a feature request form
        layout.addWidget(button_request_feature)
        button_check_for_updates = QPushButton("Check for Updates")
        button_check_for_updates.setStyleSheet("background-color: #6A5ACD; color: white;")
        button_check_for_updates.clicked.connect(lambda: updater_notification(api_handler.get_launcher_version().json()).exec_())
        layout.addWidget(button_check_for_updates)
        path_label = QLabel("Custom Steam Path:")
        layout.addWidget(path_label)
        self.path_input = QLineEdit()
        layout.addWidget(self.path_input)
        # todo Add when the Input Path field exists.
        # update_config_item("steam", "custom_path", "C:\\Program Files (x86)\\Steam\\steamapps\\libraryfolders.vdf")
        # new_config = load_config()
        # steam_parser.setup(new_config)

        self.setLayout(layout)
        logger.log(level="debug", handler="window_handler", message="Opened settings window")


class updater_notification(QDialog):
    def __init__(self, status):
        super().__init__()
        print(status)
        logger.log(level="debug", handler="window_handler", message="Opening updater message window")
        self.setWindowTitle("Checking for Updates")
        self.setGeometry(300, 300, 300, 200)
        self.setStyleSheet("background-color: #333333; color: white;")
        # status: {"version":"0.0.1"}
        layout = QVBoxLayout()
        current_version = load_config()["global"]["version"]
        new_version = status["version"]
        if current_version != new_version:
            message = f"New version available: {new_version}. Current version: {current_version}"
        else:
            message = f"No new updates available. Current version: {current_version}"
        message_label = QLabel(message)
        layout.addWidget(message_label)
        self.setLayout(layout)

class message_box(QDialog):
    def __init__(self, title, message):
        super().__init__()
        logger.log(level="debug", handler="window_handler", message="Opening message box")
        self.setWindowTitle(title)
        self.setGeometry(300, 300, 300, 200)
        self.setStyleSheet("background-color: #333333; color: white;")
        layout = QVBoxLayout()
        message_label = QLabel(message)
        layout.addWidget(message_label)
        self.setLayout(layout)
