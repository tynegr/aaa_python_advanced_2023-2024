import sys
from datetime import datetime

original_write = sys.stdout.write


def my_write(string_text):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

    original_write(f"{timestamp}: {string_text}")


sys.stdout.write = my_write
print('1, 2, 3')
sys.stdout.write = original_write
