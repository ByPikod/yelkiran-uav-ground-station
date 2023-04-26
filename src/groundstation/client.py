"""Client class for multithreading."""
from typing import Tuple

import socket as s
import threading as t
import time

from .logging import logger as log
from .utilities import PeriodicTimer


class Client:
    """
    Client class for multithreading.
    """

    socket: s.socket
    addr: Tuple[str, int]

    listen: bool = True

    thread_listening: t.Thread
    heartbeat_timer: PeriodicTimer = None

    # How much time after client will be disconnected from the moment that heartbeat stopped (second).
    heartbeat_timeout = 5
    # Heartbeat check frequency (second).
    heartbeat_check_frequency = 5
    # Last heartbeat time (epoch time).
    heartbeat_last = 0

    def __init__(
            self,
            client: s.socket,
            addr: Tuple[str, int],
            disconnected
    ) -> None:
        # Fill fields
        self.socket = client
        self.addr = addr
        self.cb_disconnected = disconnected
        # Updating heartbeat because we don't want client to get kicked just after we start checking.
        self.heartbeat_last = time.time()
        # Start listening heartbeats
        self.thread_listening = t.Thread(target=self.handle_tcp)
        self.thread_listening.start()
        # Check if connection is still available
        self.check_heartbeat()

    def check_heartbeat(self) -> None:
        """
        Checks if client is still connected.
        """
        if self.heartbeat_last + self.heartbeat_timeout > time.time():
            self.heartbeat_timer = PeriodicTimer(
                float(self.heartbeat_check_frequency),
                0.1,
                self.check_heartbeat
            )
            self.heartbeat_timer.start()
            return

        self.kick()

    def handle_tcp(self) -> None:
        """
        Handle TCP messages.
        """

        while self.listen:

            data: bytes
            try:
                data = self.socket.recv(512)
                if b"heartbeat" in data:
                    addr, port = self.socket.getsockname()
                    log().info(f"Heartbeat received: {addr}:{port}")
                    self.heartbeat_last = time.time()
            except OSError:
                self.cb_disconnected(self.socket, self.addr)
                self.kick()
                break

    def kick(self) -> None:
        """
        Terminate connection.
        """
        self.listen = False
        self.socket.close()
        if self.heartbeat_timer is not None:
            self.heartbeat_timer.cancel()
