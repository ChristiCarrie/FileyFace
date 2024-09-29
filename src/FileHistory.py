import csv

def write_to_file(file_name, file_path, timestamp):
    timestamp = timestamp.strftime(fr"%Y-%m-%d %H:%M:%S")
    print(timestamp)
    data = [str(file_name), str(file_path), str(timestamp)]
    text_file = fr'C:\Users\Aadit Bansal\FileyFace\file_history.csv'
    existing_content = []
    try:
        with open(text_file, 'r', newline='') as file:
            reader = csv.reader(file)
            existing_content = list(reader)
    except FileNotFoundError:
        existing_content = []

    data = [data] + existing_content
    
    try:
        with open(text_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    except PermissionError as E:
        return