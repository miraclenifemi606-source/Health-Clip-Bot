import os

def clean_up(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
