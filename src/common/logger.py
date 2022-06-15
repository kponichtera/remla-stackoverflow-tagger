"""Module for printing with color
"""
from enum import Enum

class Logger(Enum):
    """
    Color class.
    """
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_CYAN = '\033[96m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END_CHAR = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def info(text : str):
        """Method to print log information.

        Args:
            text (str): string to print
        """
        print(f"{Logger.OK_GREEN.value}INFO{Logger.END_CHAR.value}:     {text}")

    @staticmethod
    def warning(text : str):
        """Method to print a warning.

        Args:
            text (str): string to print
        """
        print(f"{Logger.WARNING.value}WARN{Logger.END_CHAR.value}:     {text}")

    @staticmethod
    def fail(text : str):
        """Method to print a failure or warning.

        Args:
            text (str): string to print
        """
        print(f"{Logger.FAIL.value}ERROR{Logger.END_CHAR.value}:     {text}")

    @staticmethod
    def log(colored_text : str, color):
        """Method to print with a custom color.

        Args:
            colored_text (str): string to print
            color (Logger): color from ColorsPrinter class
        """
        print(f"{color.value}{colored_text}{Logger.END_CHAR.value}")

    @staticmethod
    def get_color_string(text_to_color : str, color) -> str:
        """Add color string.

        Args:
            text_to_color (str): _description_
            color (Logger): color from ColorsPrinter class
        """
        return f"{color.value}{text_to_color}{Logger.END_CHAR.value}"
