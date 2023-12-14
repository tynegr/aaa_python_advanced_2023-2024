import sys
from datetime import datetime

original_write = sys.stdout.write


def my_write(string_text: str) -> None:
    """
    Custom write function that adds a timestamp to the output.

    Parameters:
        string_text (str): The text to be written.

    Returns:
        None
    """
    timestamp = datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
    original_write(f'{timestamp}: {string_text}')


sys.stdout.write = my_write
print('1, 2, 3')
sys.stdout.write = original_write
