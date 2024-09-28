import zipfile
import os

def unzip(file_path, folder_path):
    os.makedirs(folder_path, exist_ok=True)
    with zipfile.ZipFile(file_path, 'r') as zip:
        zip.extractall(folder_path)

# file_path = r"C:\Users\Aadit Bansal\Downloads\course_files_export.zip"
# folder_path = r"C:\Users\Aadit Bansal\FileyFace"
# unzip(file_path, folder_path)