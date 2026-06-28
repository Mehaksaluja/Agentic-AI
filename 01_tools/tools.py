from datetime import datetime

def calculator(a: float, b: float, operation: str):

    if operation == "+":
        return a + b

    elif operation == "-":
        return a - b

    elif operation == "*":
        return a * b

    elif operation == "/":
        if b == 0:
            return "Division by zero not allowed"
        return a / b

    return "Invalid operation"


def get_time():
    return datetime.now().strftime("%H:%M:%S")