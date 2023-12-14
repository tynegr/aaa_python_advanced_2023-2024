import sys
from datetime import datetime
from typing import Callable, Any


def timed_output(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator that adds a timestamp to the standard output.

    Parameters:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The wrapper function.
    """
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

    def wrapper(*args, **kwargs) -> Any:
        """
        Wrapper function that redirects the standard output and adds
         a timestamp.

        Parameters:
            *args: Variable positional arguments.
            **kwargs: Variable keyword arguments.

        Returns:
            Any: The result of the decorated function.
        """
        sys.stdout.write = my_write
        try:
            result = func(*args, **kwargs)
        finally:
            sys.stdout.write = original_write
        return result

    return wrapper


@timed_output
def print_greeting(name: str) -> None:
    """
    Prints a greeting message with a timestamp.

    Parameters:
        name (str): The name to include in the greeting.

    Returns:
        None
    """
    print(f'Hello, {name}!')


print_greeting('Nikita')
