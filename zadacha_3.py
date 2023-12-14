import sys
from typing import Callable


def redirect_output(filepath: str) -> Callable:
    """
    Decorator that redirects the standard output to a file.

    Parameters:
        filepath (str): The path to the file where the output will
        be redirected.

    Returns:
        Callable: A decorator function.
    """
    def decorator(func: Callable) -> Callable:
        """
        Decorator function that wraps the original function
        and redirects its output.

        Parameters:
            func (Callable): The function to be decorated.

        Returns:
            Callable: The wrapper function.
        """
        def wrapper(*args, **kwargs):
            original_stdout = sys.stdout
            try:
                with open(filepath, 'w') as file:
                    sys.stdout = file
                    result = func(*args, **kwargs)
            finally:
                sys.stdout = original_stdout
            return result
        return wrapper
    return decorator


@redirect_output('./function_output.txt')
def calculate_powers():
    """
    Calculates powers of numbers and prints the result to the
    redirected output.
    """
    for power in range(1, 5):
        for num in range(1, 20):
            print(num ** power, end=' ')
        print()


calculate_powers()

with open('./function_output.txt', 'r') as f:
    data = f.read()
    print(data)
