"""Application"""
import os
import datetime
import tkinter as tk

from . import server as sv
from . import logging
from .logging import Logger
from .logging import logger as log
from .config import ConfigManager
from .client import Client
from .gui import Window


class Application:
    """
    Initialize the window and server.
    """

    config: ConfigManager = None
    server: sv.Server = None
    window: Window = None

    log_directory: str | None

    def __init__(self) -> None:

        # Configuration
        self.config = ConfigManager()

        # Logger
        self.log_directory = None
        if self.config.get_bool("general.logging"):

            self.log_directory = self.config.get_string("general.logging-directory")
            self.log_directory = os.path.abspath(os.path.join(
                self.log_directory,
                f"LOG {datetime.datetime.now().strftime('%d.%m.%Y %H-%M-%S')}"
            ))

            if not os.path.exists(self.log_directory):
                os.makedirs(self.log_directory)

        logging._logger = Logger(self.log_directory)
        log().info("Logger initialized.")

        # Server
        class CustomClient(Client):
            heartbeat_timeout = self.config.get_int("server.timeout-period")
            heartbeat_check_frequency = self.config.get_int("server.timeout-check-frequency")

        sv.Client = CustomClient

        self.server = sv.Server(
            self.config.get_string("server.host"),
            self.config.get_int("server.query-port"),
            self.config.get_int("server.stream-port")
        )

        # Window

        self.root = tk.Tk()
        self.window = Window(
            self.server,
            master=self.root
        )

        self.window.set_output_size(
            self.config.get_int("appearance.video-width"),
            self.config.get_int("appearance.video-height"),
        )

        self.window.mainloop()
        self.server.terminate()
