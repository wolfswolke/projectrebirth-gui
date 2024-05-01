from logic.logging_handler import logger
from logic.setup_handlers import load_config
from logic.api_handler import api_handler


def start_app():
    pass


def check_for_updates():
    latest_gui_version = api_handler.get_launcher_version().json()
    if latest_gui_version != gui_version:
        logger.log(level="info", handler="start", message={f"New version available: {latest_gui_version}. "
                                                           f"Current version: {gui_version}"})
        return True
    else:
        return False


if __name__ == "__main__":
    config = load_config()

    name = config["global"]["name"]
    gui_version = config["global"]["version"]
    level = config["global"]["level"]
    website_url = config["urls"]["website"]
    logger.setup_logging(level=level)

    api_handler.setup(config)
    start_app()
