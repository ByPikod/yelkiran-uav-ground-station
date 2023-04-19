"""Client class for multithreading."""
import socket as s


class Client:
    socket: s.socket
    addr: tuple[str, int]

    def __init__(
            self,
            client: s.socket,
            addr: tuple[str, int],
            disconnected
    ) -> None:

        self.socket = client
        self.addr = addr

        self.cb_disconnected = disconnected

    def handle_tcp(self) -> None:
        """
        Handle TCP messages.
        :return:
        """

        while True:

            data: bytes
            try:
                data = self.socket.recv(1024)
            except OSError:
                self.cb_disconnected(self.socket, self.addr)
                self.socket.close()
                break
