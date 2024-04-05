import os

def grab_files(path):
    files = []
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))  # Sort based on numerical value in filename
    return files

