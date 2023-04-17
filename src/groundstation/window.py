"""Window"""
import pickle
import numpy as np
import tkinter as tk

import cv2
from PIL import Image, ImageTk

from .logging import logger as log


class Window(tk.Frame):
    """
    Creates the window.
    """

    label_image: tk.Label = None
    image: bytes = None

    def __init__(self, master: tk.Tk, *args, **kwargs) -> None:
        super().__init__(master=master, *args, **kwargs)
        master.title("Yelkıran - Ground Station")
        self.pack()
        self.initialize()
        log().info("Frame initialized.")

    def onclick_quit(self):
        self.quit()

    def initialize(self) -> None:
        self.label_image = tk.Label(self, text="Waiting for stream!")
        self.label_image.pack()
        quit_button = tk.Button(self, text="Quit!", command=self.onclick_quit)
        quit_button.pack()

        self.loop()

    def loop(self):
        if self.image is not None:
            img_bytes = pickle.loads(self.image)
            img_decoded: np.ndarray = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
            img_decoded = cv2.cvtColor(img_decoded, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(img_decoded)
            image_tk = ImageTk.PhotoImage(image)
            self.label_image.imgtk = image_tk
            self.label_image.configure(image=image_tk)
        self.after(5, self.loop)
