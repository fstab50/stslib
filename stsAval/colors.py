""" Summary ANSI color and formatting code class

Args:
    None

Returns:
    ansi codes
"""

class Colors():
    """
    Class attributes provide different format variations
    """
    # forground colors
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    DARKGREEN = '\u001b[38;5;2m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[37m'
    LTGRAY =  '\u001b[38;5;249m'
    DARKGRAY = '\033[90m'

    # background colors
    WHITEBKG = '\u001b[47;1m'

    # formats
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC = '\e[3m'
    END = '\033[0m'
    REVERSE = "\033[;7m"
    RESET = "\033[0;0m"
