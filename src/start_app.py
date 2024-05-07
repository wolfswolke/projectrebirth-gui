from logic.logging_handler import logger
from logic.setup_handlers import load_config
from logic.api_handler import api_handler
from logic.file_handler import file_handler
from logic.steam_parser import steam_parser
from logic.window_handler import MainWindow

# Testing / Handling imports
import threading
import time
import json

# QT Imports
from PyQt5.QtWidgets import QApplication
import sys


api_status = False
lock = threading.Lock()


def start_app():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


def check_for_updates():
    latest_gui_version = api_handler.get_launcher_version().json()
    if latest_gui_version != gui_version:
        logger.log(level="info", handler="start", message={f"New version available: {latest_gui_version}. "
                                                           f"Current version: {gui_version}"})
        return True
    else:
        return False


def get_health():
    global api_status
    try:
        health_check_result = api_handler.get_healthcheck()
        if health_check_result.json()["Health"] == "Alive":
            with lock:
                api_status = True
        else:
            with lock:
                api_status = False
    except Exception as e:
        with lock:
            api_status = False
        print("Error checking API health:", e)


def update_health_thread():
    while True:
        get_health()
        time.sleep(5)


if __name__ == "__main__":
    try:
        config = load_config()

        name = config["global"]["name"]
        gui_version = config["global"]["version"]
        level = config["global"]["level"]
        website_url = config["urls"]["website"]
        custom_path = config["steam"]["custom_path"]
        patched_game_ids = config["patched_games"]["ids"]
        logger.setup_logging(level=level)
        api_handler.setup(config)

        api_thread = threading.Thread(target=update_health_thread)
        api_thread.daemon = True
        api_thread.start()

        check_for_updates()

        if custom_path != "":
            steam_parser.setup(custom_path)
            logger.log(level="debug", handler="start", message=f"Custom steam path set. Setting to: {custom_path}")
        steam_parser.parse()

        # todo REMOVE this testing code when done TM
        while True:
            logger.log(level="info", handler="start", message=f"API Status: {api_status}")
            logger.log(level="debug", handler="start", message="STARING MAIN WINDOW")
            logger.log(level="debug", handler="start", message="----------------------------------------------------")
            start_app()
            time.sleep(50)
    except KeyboardInterrupt:
        logger.log(level="info", handler="start", message="Shutting down")
        exit(0)
