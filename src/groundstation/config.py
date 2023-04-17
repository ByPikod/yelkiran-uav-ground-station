"""Configuration management."""
import configparser
import os


class ConfigManager:
    """
    Config utils.
    """

    config_parser: configparser.ConfigParser

    @staticmethod
    def fill_config(conf: configparser.ConfigParser):
        """
        Fills the ConfigParser that passed as an argument with the default config variables.
        """

        conf["GENERAL"] = {
            "logging": True,
            "logging-directory": "./logs/"
        }

        conf["SERVER"] = {
            "host": "0.0.0.0",
            "port": "1864"
        }

    def __init__(self):

        # Create a config
        self.config_parser = configparser.ConfigParser()

        # Fill with default variables
        self.fill_config(self.config_parser)

        # Read data
        root_dir = os.path.dirname(os.path.abspath(__file__))
        self.conf_path = os.path.join(root_dir, "configuration.ini")
        self.config_parser.read(self.conf_path)

        # Write data
        self.save()

    def get_string(self, locator: str) -> str:
        """
        Allows you to retrieve config data quickly.
        You can write "simulator.enabled" instead ["SIMULATOR"]["enabled"]
        """
        split_locator = locator.split(".")
        split_locator[0] = split_locator[0].upper()

        return self.config_parser[split_locator[0]][split_locator[1]]

    def get_bool(self, field: str) -> bool:
        """Returns bool data from config."""

        return self.get_string(field).lower() == "true"

    def get_int(self, field: str) -> int:
        """Returns int data from config."""

        try:
            return int(self.get_string(field))
        except ValueError:
            return 0

    def set_field(self, locator: str, value: any) -> None:
        """
        Allows you to write config data quickly.
        You can write "simulator.enabled" instead ["SIMULATOR"]["enabled"]
        """
        split_locator = locator.split(".")
        split_locator[0] = split_locator[0].upper()

        self.config_parser[split_locator[0]][split_locator[1]] = value

    def save(self) -> None:
        """Write config."""

        with open(self.conf_path, 'w') as conf_file:
            self.config_parser.write(conf_file)
