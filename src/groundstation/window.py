"""Window"""
import tkinter as tk

from .logging import logger as log


class Window(tk.Frame):
    """Creates the window"""

    def __init__(self, master: tk.Tk, *args, **kwargs) -> None:
        super().__init__(master=master, *args, **kwargs)
        master.title("Yelkıran - Ground Station")
        self.pack()
        self.initialize()
        log().info("Frame initialized.")

    def initialize(self) -> None:
        pass
