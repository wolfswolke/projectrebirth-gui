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
            # Try to get games
            games = api_handler.get_games()
            for game_content in games["games"]:
                logger.log(level="info", handler="start", message=f"Found game: {game_content['name']}")
                logger.log(level="info", handler="start", message=f"ID: {game_content['id']}, status: {game_content['status']}, image_url: {game_content['image']}")
                # Try to get one games content
                game_id = game_content["id"]
                game = api_handler.get_game(game_id)
                logger.log(level="info", handler="start", message=f"Game Info: {game.json()}")
                # Get Patch
                patch = api_handler.get_patch(game_id)
                logger.log(level="info", handler="start", message=f"Patch for this game: {patch.json()}")
            # Try searching for games
            test_ids = [555440, 228980, 111111111111111111111111]
            # DGBH and Steamworks and something that should not exist
            for game_id in test_ids:
                game = steam_parser.get_path(game_id)
                logger.log(level="info", handler="start", message=f"Path for {game_id}: {game}")

            start_app()
            time.sleep(50)
    except KeyboardInterrupt:
        logger.log(level="info", handler="start", message="Shutting down")
        exit(0)
