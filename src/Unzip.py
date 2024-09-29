import zipfile
import os

def unzip(file_path, folder_path):
    os.makedirs(folder_path, exist_ok=True)
    with zipfile.ZipFile(file_path, 'r') as zip:
        zip.extractall(folder_path)

