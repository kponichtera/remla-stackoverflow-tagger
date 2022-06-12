"""Module for printing with color
"""
from enum import Enum

class ColorsPrinter(Enum):
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
    def log_print_info(text : str):
        """Method to print log information.

        Args:
            text (str): string to print
        """
        print(f"{ColorsPrinter.OK_GREEN.value}INFO{ColorsPrinter.END_CHAR.value}:     {text}")

    @staticmethod
    def log_print_warning(text : str):
        """Method to print a warning.

        Args:
            text (str): string to print
        """
        print(f"{ColorsPrinter.WARNING.value}WARN{ColorsPrinter.END_CHAR.value}:     {text}")

    @staticmethod
    def log_print_fail(text : str):
        """Method to print a failure or warning.

        Args:
            text (str): string to print
        """
        print(f"{ColorsPrinter.FAIL.value}ERROR{ColorsPrinter.END_CHAR.value}:     {text}")

    @staticmethod
    def log_print_custom(colored_text : str, color):
        """Method to print with a custom color.

        Args:
            colored_text (str): string to print
            color (ColorsPrinter): color from ColorsPrinter class
        """
        print(f"{color.value}{colored_text}{ColorsPrinter.END_CHAR.value}")

    @staticmethod
    def get_color_string(text_to_color : str, color):
        """Add color string.

        Args:
            text_to_color (str): _description_
            color (ColorsPrinter): color from ColorsPrinter class
        """
        return f"{color.value}{text_to_color}{ColorsPrinter.END_CHAR.value}"
