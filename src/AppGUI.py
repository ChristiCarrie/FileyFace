import os
import time
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import Requests
from Unzip import unzip

# Set source root folder path (default=Downloads)
SRC_ROOT = os.path.expanduser("~/Downloads")

USERNAME = os.environ.get('USER') or os.environ.get('USERNAME')

class FileHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        #self.processed_files = set()
        
    def on_modified(self, event):
        # Ignore directory creation events
        if event.is_directory:
            return
        
        time.sleep(0.3)
        file_name = os.path.basename(event.src_path)
        print(f"Detected change: {file_name}")      # Temp debug statement
        
        # Logic to ignore temporary files
        if file_name.endswith(('.tmp', '.crdownload', '.ini')):
            print(f"Ignoring temporary and other system files: {file_name}")     # Temp debug statement        
            return
        else:
            print(f"Processing file: {file_name}")      # Temp debug statement
            #if file_name not in self.processed_files:
                #self.processed_files.add(file_name)
            self.organize_file(file_name)
            # else:
            #     print(f"'{file_name}' has already been processed.")     # Temp debug statement
                
    def organize_file(self, file_name):
        src_file_path = os.path.join(SRC_ROOT, file_name)
        additional_suggestions = ''
        
        regenerate = True
        while (regenerate):
            # Check if the file still exists
            if not os.path.exists(src_file_path):
                print(f"Source file '{src_file_path}' does not exist. Skipping.")
                return
            
            dst_file_filepath = Requests.ask_for_file(src_file_path, USERNAME, additional_suggestions)
            dst_file_filepath = Path(str(dst_file_filepath))
            print(dst_file_filepath)
            
            # Prompt the user for confirmation to move the file
            user_response = self.prompt_user(file_name, dst_file_filepath)
            if user_response[0]:
                
                file_ext = os.path.splitext(file_name)[1]
                final_file_name = user_response[1] + file_ext
                
                if user_response[0] == 'REGEN':
                    additional_suggestions = user_response[2]
                    continue
                else:
                    try:
                        time.sleep(0.2)
                        os.makedirs(dst_file_filepath.parent, exist_ok=True)
                        if file_ext != '.zip':
                            print('here1')            
                            dst_file_filepath = dst_file_filepath.parent / final_file_name
                            os.rename(src_file_path, dst_file_filepath)
                            #print(f"Moved '{file_name}' to '{dst_file_filepath.parent}' as '{final_file_name}'")
                        else:
                            #print('here2')
                            unzip(src_file_path, dst_file_filepath.parent)
                            time.sleep(4)
                    except FileExistsError as E:
                        print('File already exists at specified location - left in Downloads')
                    finally:
                        regenerate = False
            else:
                regenerate = False
        

    def prompt_user(self, file_name, destination_folder):
        print(f"Prompting user to move '{file_name}' to '{destination_folder}'")  # Debug statement

        # Create a new top-level window for user input
        prompt_window = tk.Tk()
        prompt_window.title("FileyFace")
        prompt_window.attributes('-topmost', True)  # Make the window stay on top
        # prompt_window.geometry("400x200+500+500")  # Set the size of the window MAKE THIS BIGGER OR SMALLER ACCORDINGLY

        popup_width = 600
        popup_height = 300

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
        small_icon = Image.open("./Website/FileyFaceLogo.png")
        small_icon = small_icon.resize((32, 32), Image.Resampling.LANCZOS)  # Use 32x32 for the title bar icon size
        small_icon_image = ImageTk.PhotoImage(small_icon)
        prompt_window.iconphoto(False, small_icon_image)  # Set the window icon

        tk.Label(prompt_window, text="Do you want to move:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)

        # Get the original file name without extension
        base_file_name = os.path.splitext(file_name)[0]
        file_extension = os.path.splitext(file_name)[1]

        # Create a frame to hold the entry and label
        input_frame_1 = tk.Frame(prompt_window, bg="#f0f0f0")
        input_frame_1.pack(pady=5)

        # Create the entry for the new file name
        new_file_name_entry = tk.Entry(input_frame_1, font=("Arial", 12), width=30)
        new_file_name_entry.insert(0, base_file_name)  # Default to the base name
        new_file_name_entry.pack(side=tk.LEFT)  # Place it on the left side

        # Create the label for the file extension
        extension_label = tk.Label(input_frame_1, text=file_extension, bg="#f0f0f0", font=("Arial", 12))
        extension_label.pack(side=tk.LEFT)  # Place it on the right side

        # Update the label to show the correct prompt
        tk.Label(prompt_window, text=f"to '{destination_folder}'?", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
        # tk.Label(prompt_window, text=f"Do you want to move '{new_file_name_entry.get()} {file_extension}' to '{destination_folder}'?", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)

        tk.Label(prompt_window, text=f"Add suggestions or desired file locations below:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
        
        # Create another frame to hold the suggestion entry
        input_frame_2 = tk.Frame(prompt_window, bg="#f0f0f0")
        input_frame_2.pack(pady=5)
        
        # Create the entry for the user suggestions to the AI
        suggestions_entry = tk.Entry(input_frame_2, font=("Arial", 12), width=30)
        suggestions_entry.pack(side=tk.LEFT)

        # Variable to store user choice
        user_choice = [None, None, None]

        def on_yes():
            user_choice[0] = 'YES'
            user_choice[1] = new_file_name_entry.get().strip()  
            prompt_window.destroy() 

        def on_regen():
            user_choice[0] = 'REGEN'
            user_choice[1] = new_file_name_entry.get().strip()
            user_choice[2] = suggestions_entry.get().strip()
            prompt_window.destroy()

        def on_no():
            user_choice[0] = None       # Indicate to keep the file in Downloads
            prompt_window.destroy()

        button_frame = tk.Frame(prompt_window, bg="#f0f0f0")  # Frame for buttons
        button_frame.pack(pady=20)

        yes_button = tk.Button(button_frame, text="Yes", command=on_yes, font=("Arial", 12), bg="#4CAF50", fg="white")
        yes_button.pack(side=tk.LEFT, padx=10)

        regen_button = tk.Button(button_frame, text="Regenerate", command=on_regen, font=("Arial", 12), bg="#eb9336", fg="white")
        regen_button.pack(side=tk.LEFT, padx=10)
        no_button = tk.Button(button_frame, text="No", command=on_no, font=("Arial", 12), bg="#f44336", fg="white")
        no_button.pack(side=tk.RIGHT, padx=10)

        prompt_window.protocol("WM_DELETE_WINDOW", prompt_window.destroy)  # Handle window close
        prompt_window.mainloop()  # Start the event loop

        return user_choice  # Return the user's choice

def start_monitoring():
    observer = Observer()
    event_handler = FileHandler()
    observer.schedule(event_handler, SRC_ROOT, recursive=False)
    observer.start()
    print(f"Monitoring folder: {SRC_ROOT}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_monitoring()
    