import logging
import sys
import json
import traceback
from colorlog import ColoredFormatter


class Logger:
    def __init__(self):
        self.my_logger = logging.getLogger('project_rebirth_gui')

    def setup_logging(self, level):
        if level == "debug":
            self.my_logger.setLevel(logging.DEBUG)
        elif level == "info":
            self.my_logger.setLevel(logging.INFO)
        elif level == "warning":
            self.my_logger.setLevel(logging.WARNING)
        elif level == "error":
            self.my_logger.setLevel(logging.ERROR)
        elif level == "critical":
            self.my_logger.setLevel(logging.CRITICAL)
        else:
            print("ERROR: No valid log level specified.")
            sys.exit(1)
        self.log(level="debug", handler="logging_logic_event", message={"event": "Logging initialized."})

    def log(self, level, handler, message):
        formatter = ColoredFormatter(
            "%(log_color)s%(asctime)s %(levelname)-8s%(reset)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            reset=True,
            log_colors={
                'DEBUG': 'blue',
                'INFO': 'white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self.my_logger.addHandler(console_handler)
        log_methods = {"debug": self.my_logger.debug, "warning": self.my_logger.warning,
                       "error": self.my_logger.error, "info": self.my_logger.info,
                       "critical": self.my_logger.critical}
        log_method = log_methods.get(level)
        if log_method:
            try:
                message = json.dumps({"level": level, "handler": handler, "message": message})
            except TypeError:
                message = f"{{\"level\": \"{level}\", \"handler\": \"{handler}\", \"message\": \"{str(message)}\"}}"
            if level == "error":
                exc_type, exc_value, exc_traceback = sys.exc_info()
                tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
                message = f"{message}\n{''.join(tb_str)}"

            log_method(message)
        else:
            print("ERROR: No valid log level specified.")
        self.my_logger.removeHandler(console_handler)


logger = Logger()
