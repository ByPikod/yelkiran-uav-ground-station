"""Server"""
import threading as t
import socket as s

from .logging import logger as log


class Server:
    """
    Initialize server.
    """

    server: s.socket
    thread: t.Thread

    addr: tuple[str, int]
    client_addr: tuple[str, int]

    running: bool = True

    def __init__(self, addr: tuple[str, int], update_image) -> None:
        # Create socket instance
        self.server = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.server.bind(addr)

        self.callback = update_image
        # Start Loop
        self.thread = t.Thread(target=self.mainloop)
        self.thread.start()
        log().info("Server initialized.")

    def mainloop(self) -> None:
        """Accept connection request."""

        while self.running:

            # Receive
            data: bytes = b''
            try:
                data = self.server.recv(60000)
            except OSError:
                print("listening")
                continue

            # Pass the data
            self.callback(data)
