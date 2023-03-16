import logging
from os.path import dirname, join
from datetime import date

from utils.system_manager import SystemManager


class Logger(logging.Logger):
    def __init__(self, name, level=logging.INFO, filepath=None):
        super().__init__(name, level)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s ; %(levelname)s ; %(filename)s ; %(message)s')

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Create file handler
        filepath = filepath or join("logs", name)
        SystemManager.create_folder(dirname(filepath))
        file_handler = logging.FileHandler(filepath)
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)

        # Add handlers to logger
        self.addHandler(console_handler)

    @staticmethod
    def extract_errors():
        errors = []
        with open(f"logs/{date.today():%Y%m%d}.log") as file:
            for log in file:
                if "; ERROR ;" in log:
                    errors.append(log.split(' ; ')[-1])
        return errors


logger = Logger("Limit Check Logger", filepath=join("logs", f"{date.today():%Y%m%d}.log"))
