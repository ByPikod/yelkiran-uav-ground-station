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
    """
    Initialize the window and server.
    """

    config: ConfigManager = None
    server: Server = None
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

        # Window
        self.root = tk.Tk()
        self.window = Window(master=self.root)

        # Server
        def update_image(image: bytes) -> None:
            """
            Callback to update image in the window.
            """
            self.window.image = image

        self.server = Server(
            (
                self.config.get_string("server.host"),
                self.config.get_int("server.port")
            ),
            update_image
        )

        # Start window loop
        self.window.mainloop()
        self.server.running = False
        self.server.server.close()
