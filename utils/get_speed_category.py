from config import *

def get_speed_category(elapsed_seconds):
    if elapsed_seconds < SLOW_THRESHOLD:
        return SLOW_FOLDER
    elif elapsed_seconds < MEDIUM_THRESHOLD:
        return MEDIUM_FOLDER
    else:
        return FAST_FOLDER