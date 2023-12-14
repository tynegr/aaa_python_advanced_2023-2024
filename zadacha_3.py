import sys


def redirect_output(filepath):
    def decorator(func):
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
def calculate():
    for power in range(1, 5):
        for num in range(1, 20):
            print(num ** power, end=' ')
        print()


calculate()
with open('./function_output.txt', 'r') as f:
    content = f.read()
    print(content)
