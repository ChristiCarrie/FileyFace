import time
import os
import shutil
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Ignore directory creation events
        if event.is_directory:
            return

        # Wait for the file to be fully downloaded
        time.sleep(1)
        self.process_new_file(event.src_path)

    def process_new_file(self, file_path):
        file_name, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()

        # Define your destination directories
        destination_directories = {
            '.jpg': 'Images',
            '.jpeg': 'Images',
            '.png': 'Images',
            '.gif': 'Images',
            '.pdf': 'Documents',
            '.docx': 'Documents',
            '.doc': 'Documents',
            '.txt': 'Documents',
            '.mp3': 'Music',
            '.wav': 'Music',
            '.mp4': 'Videos',
            '.mov': 'Videos',
            # Add more extensions and categories as needed
        }

        # Get the base directory of the file
        base_dir = os.path.dirname(file_path)

        # Determine the destination directory
        destination_dir_name = destination_directories.get(file_extension, 'Others')
        destination_dir = os.path.join(base_dir, destination_dir_name)

        # Create the destination directory if it doesn't exist
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # Move the file
        self.move_file(file_path, destination_dir)

    def move_file(self, src_path, dest_dir):
        file_name = os.path.basename(src_path)
        dest_path = os.path.join(dest_dir, file_name)

        # Check if file exists
        if os.path.exists(dest_path):
            # Create a unique file name
            base, extension = os.path.splitext(file_name)
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            new_file_name = f"{base}_{timestamp}{extension}"
            dest_path = os.path.join(dest_dir, new_file_name)

        try:
            shutil.move(src_path, dest_path)
            print(f"Moved '{src_path}' to '{dest_path}'")
        except Exception as e:
            print(f"Error moving file '{src_path}': {e}")

if __name__ == "__main__":
    # Specify the directory to monitor
    monitor_directory = "C:/Users/xtoml/Desktop/giggle" 

    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=monitor_directory, recursive=False)
    observer.start()
    print(f"Monitoring started on directory: {monitor_directory}")

    try:
        while True:
            time.sleep(10)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()