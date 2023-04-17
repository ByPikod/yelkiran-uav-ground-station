"""Server"""
import socket as s
import threading as t

from .logging import logger as log


class Server:
    """Initialize server."""

    server: s.socket
    thread: t.Thread

    addr: tuple[str, int]

    def __init__(self, addr: tuple[str, int]) -> None:
        self.server = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.server.bind(addr)
        self.thread = t.Thread(target=self.mainloop)
        log().info("Server initialized.")

    def mainloop(self) -> None:
        self.server.listen(1)
