"""Application"""
import os
import datetime
import tkinter as tk

from . import logging
from .logging import Logger
from .logging import logger as log
from .config import ConfigManager
from .window import Window
from .server import Server


class Application:
    """Initialize the window and server."""

    config: ConfigManager
    server: Server
    window: Window

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
        self.server = Server(
            (
                self.config.get_string("server.host"),
                self.config.get_int("server.port")
            )
        )

        # Window
        self.root = tk.Tk()
        self.window = Window(master=self.root)
        self.window.mainloop()
