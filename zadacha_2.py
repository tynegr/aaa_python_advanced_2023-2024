import sys
from datetime import datetime


def timed_output(func):
    original_write = sys.stdout.write

    def my_write(string_text):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        original_write(f"{timestamp}: {string_text}")

    def wrapper(*args, **kwargs):
        sys.stdout.write = my_write
        try:
            result = func(*args, **kwargs)
        finally:
            sys.stdout.write = original_write
        return result

    return wrapper


@timed_output
def print_greeting(name):
    print(f'Hello, {name}!')


print_greeting("Nikita")
