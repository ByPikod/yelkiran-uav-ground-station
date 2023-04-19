"""Server"""
import threading as t
import socket as s

from .logging import logger as log
from .client import Client


class Server:
    """
    Initialize server.
    """

    udp_server: s.socket
    tcp_server: s.socket
    client: Client | None = None

    tcp_thread: t.Thread
    udp_thread: t.Thread

    addr: tuple[str, int]
    stream_dump: bytes = None

    running: bool = True

    def __init__(self, host: str, tcp_port: int, udp_port: int) -> None:
        # Create socket instances
        self.tcp_server = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.tcp_server.bind((host, tcp_port))
        self.tcp_server.listen(1)
        self.udp_server = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.udp_server.bind(("0.0.0.0", udp_port))

        # Start Loop
        self.udp_thread = t.Thread(target=self.handle_udp)
        self.udp_thread.start()
        self.tcp_thread = t.Thread(target=self.handle_tcp)
        self.tcp_thread.start()
        log().info("Server initialized.")
        log().info(f"Listening on *:{tcp_port} and *:{udp_port}")

    def handle_tcp(self) -> None:
        """
        Accept connection requests.
        """

        while self.running:
            # Accept any connection
            try:
                client_socket, client_addr = self.tcp_server.accept()
            except Exception as e:
                if not self.running:
                    break
                log().error(f"Failed to accept client: {e}")
                continue
            # Client connected
            self.client = Client(client_socket, client_addr, self.on_disconnected)
            self.on_connected()

            # Wait until connection broke
            self.client.handle_tcp()

    def handle_udp(self) -> None:
        """
        Listen UDP and update image.
        """

        while self.running:
            if self.client is None:
                continue

            # Listen for packets
            data: bytes = b''
            addr: tuple[str, int] = ('', 0)

            try:
                data, addr = self.udp_server.recvfrom(60000)
            except Exception as e:
                if not self.running:
                    return
                print(f"Failed to read UDP stream: {e}")

            if (
                addr[0] == self.client.addr[0]
            ):
                self.stream_dump = data

    def terminate(self) -> None:
        """
        Terminate server safely.
        """

        self.running = False

        if self.client is not None:
            self.client.socket.close()

        self.tcp_server.close()
        self.udp_server.close()

    def on_connected(self) -> None:
        """
        Client connected event.
        """

        log().info(f"Client connected: {self.client.addr[0]}:{self.client.addr[1]}")

    def on_disconnected(self, socket: s.socket, addr: tuple[str, int]) -> None:
        """
        On socket disconnected event
        :param socket: Socket
        :param addr: Host and port
        """

        log().info(f"Client disconnected: {addr[0]}:{addr[1]}")
        self.client = None
