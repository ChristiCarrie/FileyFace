import os
import time
import tkinter as tk
from PIL import Image, ImageTk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set the Downloads folder path
DOWNLOAD_FOLDER = os.path.expanduser("~/Downloads")

class FileHandler(FileSystemEventHandler):
    def _init_(self):
        super()._init_()
        self.processed_files = set()  # To keep track of processed files

    def on_modified(self, event):
        # Check if a file was created in the Downloads folder
        if not event.is_directory:
            file_name = os.path.basename(event.src_path)
            print(f"Detected change: {file_name}")  # Debug statement
            
            # Check if the file has a complete extension

            if file_name.endswith(('.tmp', '.crdownload')):  
                print(f"Ignoring temporary file: {file_name}")  # Debug statement
                return
            else:
                print(f"Processing file: {file_name}")  # Debug statement
                if file_name not in self.processed_files:  # Only process if not already processed
                    self.processed_files.add(file_name)
                    self.organize_file(file_name, event.src_path)
                else:
                    print(f"'{file_name}' has already been processed. Ignoring.")  # Debug statement

    def organize_file(self, file_name, file_path):
        folder_name = self.determine_folder(file_name)
        if folder_name:
            destination_folder = os.path.join(DOWNLOAD_FOLDER, folder_name)
            os.makedirs(destination_folder, exist_ok=True)  # Create folder if it doesn't exist

            # Prompt user for confirmation to move the file
            new_file_name = self.prompt_user(file_name, destination_folder)
            if new_file_name is not None:
                if new_file_name:  # If the user entered a new name
                    file_extension = os.path.splitext(file_name)[1]  # Get the original file extension
                    final_file_name = new_file_name + file_extension  # Combine new name with original extension
                    os.rename(file_path, os.path.join(destination_folder, final_file_name))
                    print(f"Moved '{file_name}' to '{destination_folder}' as '{final_file_name}'")
                else:  # If the user left the entry empty
                    print(f"'{file_name}' remains in Downloads.")
            else:
                print(f"'{file_name}' remains in Downloads.")
        else:
            print(f"No folder name determined for {file_name}. File will remain in Downloads.")

    def determine_folder(self, file_name):
        # Define keywords for categorization
        if 'cs2110' in file_name.lower():
            return 'cs2110'
        elif 'personal' in file_name.lower():
            return 'personal'
        elif 'work' in file_name.lower():
            return 'work'
        elif 'project' in file_name.lower() or 'projects' in file_name.lower():
            return 'projects'
        else:
            return 'other'  # Default folder for unrecognized files

    def prompt_user(self, file_name, destination_folder):
        print(f"Prompting user to move '{file_name}' to '{destination_folder}'")  # Debug statement

        # Create a new top-level window for user input
        prompt_window = tk.Tk()
        prompt_window.title("FileyFace")
        prompt_window.attributes('-topmost', True)  # Make the window stay on top
        # prompt_window.geometry("400x200+500+500")  # Set the size of the window MAKE THIS BIGGER OR SMALLER ACCORDINGLY

        popup_width = 400
        popup_height = 200

        # get the screen dimension
        screen_width = prompt_window.winfo_screenwidth()
        screen_height = prompt_window.winfo_screenheight()

        # find the center point
        center_x = int(screen_width/2 - popup_width / 2)
        center_y = int(screen_height/2 - popup_height / 2)

        # set the position of the window to the center of the screen
        prompt_window.geometry(f'{popup_width}x{popup_height}+{center_x}+{center_y}')

        # Set a theme color
        prompt_window.configure(bg="#f0f0f0")  # Light gray background


        # Set the small window icon (this is for the title bar)
        small_icon = Image.open("FileyFaceLogo.png")
        small_icon = small_icon.resize((32, 32), Image.Resampling.LANCZOS)  # Use 32x32 for the title bar icon size
        small_icon_image = ImageTk.PhotoImage(small_icon)
        prompt_window.iconphoto(False, small_icon_image)  # Set the window icon

        tk.Label(prompt_window, text="Do you want to move:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)

        # Get the original file name without extension
        base_file_name = os.path.splitext(file_name)[0]
        file_extension = os.path.splitext(file_name)[1]

        # Create a frame to hold the entry and label
        input_frame = tk.Frame(prompt_window, bg="#f0f0f0")
        input_frame.pack(pady=5)  # Pack the frame

        # Create the entry for the new file name
        new_file_name_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
        new_file_name_entry.insert(0, base_file_name)  # Default to the base name
        new_file_name_entry.pack(side=tk.LEFT)  # Place it on the left side

        # Create the label for the file extension
        extension_label = tk.Label(input_frame, text=file_extension, bg="#f0f0f0", font=("Arial", 12))
        extension_label.pack(side=tk.LEFT)  # Place it on the right side

        # Update the label to show the correct prompt
        tk.Label(prompt_window, text=f"to '{destination_folder}'?", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
        # tk.Label(prompt_window, text=f"Do you want to move '{new_file_name_entry.get()} {file_extension}' to '{destination_folder}'?", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)

        # Variable to store user choice
        user_choice = [None]  # Using a list to hold reference

        def on_yes():
            user_choice[0] = new_file_name_entry.get().strip()  # Get new file name
            prompt_window.destroy()  # Close the prompt window

        def on_no():
            user_choice[0] = None  # Indicate to keep the file in Downloads
            prompt_window.destroy()  # Close the prompt window

        button_frame = tk.Frame(prompt_window, bg="#f0f0f0")  # Frame for buttons
        button_frame.pack(pady=20)

        yes_button = tk.Button(button_frame, text="Yes", command=on_yes, font=("Arial", 12), bg="#4CAF50", fg="white")
        yes_button.pack(side=tk.LEFT, padx=10)

        no_button = tk.Button(button_frame, text="No", command=on_no, font=("Arial", 12), bg="#f44336", fg="white")
        no_button.pack(side=tk.RIGHT, padx=10)

        prompt_window.protocol("WM_DELETE_WINDOW", prompt_window.destroy)  # Handle window close
        prompt_window.mainloop()  # Start the event loop

        return user_choice[0]  # Return the user's choice

def start_monitoring():
    observer = Observer()
    event_handler = FileHandler()
    observer.schedule(event_handler, DOWNLOAD_FOLDER, recursive=False)
    observer.start()
    print(f"Monitoring folder: {DOWNLOAD_FOLDER}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_monitoring()