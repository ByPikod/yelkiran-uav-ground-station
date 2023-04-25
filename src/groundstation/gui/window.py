"""Window"""
from typing import Tuple

import pickle
import tkinter as tk

import cv2
import numpy as np
from PIL import Image, ImageTk

from ..server import Server
from ..logging import logger as log
from .button import Button


class Window(tk.Frame):
    """
    Creates the window.
    """

    label_image: tk.Label = None
    output: Tuple[int, int] = (1280, 720)
    server: Server

    def __init__(
            self,
            server: Server,
            master: tk.Tk,
            *args,
            **kwargs
    ) -> None:
        super().__init__(master=master, *args, **kwargs)

        self.root = master
        self.server = server
        master.title("Yelkıran - Ground Station")

        self.pack(padx=20, pady=20)
        self.initialize()

        log().info("Frame initialized.")

    def set_output_size(self, width, height) -> None:
        """
        Set video output size.
        :param width: Width in pixels
        :param height: Height in pixels
        """

        self.output = (width, height)

    def onclick_quit(self):
        """
        On clicked quit.
        """

        self.quit()

    def initialize(self) -> None:
        """
        Initialize window.
        """

        self.create_widgets()
        self.get_stream()
        self.ui_updates()

    def create_widgets(self) -> None:
        """
        Create widgets.
        """

        # Connection state text
        self.state_text = tk.Label(self, text="Connecting to the server.")
        self.state_text.pack(pady=10)

        # Image Output
        self.label_image = tk.Label(self, text="Waiting for stream!")
        self.label_image.pack()

        # Controls frame
        controls = tk.Frame(self)
        controls.pack(padx=10, pady=10, side=tk.BOTTOM)

        # Quit Button
        close_btn = Button(master=controls, text="Quit", command=self.onclick_quit, width=36)
        close_btn.pack()

    def ui_updates(self) -> None:
        """
        UI Updates such as server state according to server dump.
        """

        self.after(150, self.ui_updates)

    def get_stream(self) -> None:
        """
        Get stream to the frame.
        """

        if self.server.stream_dump is not None:
            img_bytes = pickle.loads(self.server.stream_dump)
            img_decoded: np.ndarray = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
            img_decoded = cv2.cvtColor(img_decoded, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(img_decoded)
            image_tk = ImageTk.PhotoImage(image.resize(self.output))
            self.label_image.imgtk = image_tk
            self.label_image.configure(image=image_tk)

        self.after(5, self.get_stream)
