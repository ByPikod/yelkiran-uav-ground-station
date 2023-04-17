import datetime
import sys
import os


class CustomOut:
    """
    This class saves prints into a log file.
    """

    def __init__(self, filename: str, std, format_message=False) -> None:
        self.console = std
        self.file = open(filename, 'w')
        self.format_msg = format_message

    def write(self, message) -> None:
        """Write override."""

        self.console.write(message)

        # Write logs
        self.file.write(message)
        self.file.flush()
        os.fsync(self.file.fileno())

    def flush(self) -> None:
        """Flush override."""

        self.console.flush()
        self.file.flush()
        os.fsync(self.file.fileno())


class Logger:
    """
    Initialize logging and print formatting systems.
    """

    def __init__(self, directory: str = None) -> None:

        # Logging enabled?
        if directory is not None:

            # Create directory if it doesn't exist.
            if not os.path.exists(directory):
                os.mkdir(directory)

            sys.stdout = CustomOut(os.path.join(directory, "stdout.txt"), sys.stdout, True)  # Stdout
            sys.stderr = CustomOut(os.path.join(directory, "stderr.txt"), sys.stderr)  # Stderr

    def info(self, message: str) -> None:
        """Print info message"""
        message = f"INFO: {message}"
        self.__write(message)

    def warn(self, message: str) -> None:
        """Print warning message"""
        message = f"WARN: {message}"
        self.__write(message)

    def error(self, message: str) -> None:
        """Print error message"""
        message = f"ERROR: {message}"
        self.__write(message)

    @staticmethod
    def __write(message: str) -> None:
        """Print any message"""
        message = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {message}\n"
        sys.stdout.write(message)


_logger: Logger | None = None


def logger() -> Logger:
    global _logger
    return _logger
