""" Summary ANSI color and formatting code class

Args:
    None

Returns:
    ansi codes
"""

class color():
    """
    Class attributes provide different format variations
    """
    # colors
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[37m'
    LTGRAY = '\033[253m'
    DARKGRAY = '\033[90m'

    # formats
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC = '\e[3m'
    END = '\033[0m'
