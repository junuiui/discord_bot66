from datetime import datetime

def timestamp():
    current_time = datetime.now().strftime()
    return "Current Time =", current_time("%H:%M:%S")