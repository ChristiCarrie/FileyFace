import os
import time
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import Requests
from Unzip import unzip


SRC_ROOT = os.path.expanduser("~/Downloads")

USERNAME = os.environ.get('USER') or os.environ.get('USERNAME')

class FileHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()

    def on_modified(self, event):

        if event.is_directory:
            return
        
        time.sleep(0.3)
        file_name = os.path.basename(event.src_path)
        print(f"Detected change: {file_name}")
        

        if file_name.endswith(('.tmp', '.crdownload', '.ini')):
            print(f"Ignoring temporary and other system files: {file_name}")  
            return
        else:
            print(f"Processing file: {file_name}")
            
            self.organize_file(file_name)

                
    def organize_file(self, file_name):
        src_file_path = os.path.join(SRC_ROOT, file_name)
        additional_suggestions = ''
        
        regenerate = True
        while (regenerate):

            if not os.path.exists(src_file_path):
                print(f"Source file '{src_file_path}' does not exist. Skipping.")
                return
            
            dst_file_filepath = Requests.ask_for_file(src_file_path, USERNAME, additional_suggestions)
            dst_file_filepath = Path(str(dst_file_filepath))
            print(dst_file_filepath)
            

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

                        else:

                            unzip(src_file_path, dst_file_filepath.parent)
                            time.sleep(4)
                    except FileExistsError as E:
                        print('File already exists at specified location - left in Downloads')
                    finally:
                        regenerate = False
            else:
                regenerate = False
        

    def prompt_user(self, file_name, destination_folder):
        print(f"Prompting user to move '{file_name}' to '{destination_folder}'")


        prompt_window = tk.Tk()
        prompt_window.title("FileyFace")
        prompt_window.attributes('-topmost', True)

        popup_width = 600
        popup_height = 300


        screen_width = prompt_window.winfo_screenwidth()
        screen_height = prompt_window.winfo_screenheight()


        center_x = int(screen_width/2 - popup_width / 2)
        center_y = int(screen_height/2 - popup_height / 2)


        prompt_window.geometry(f'{popup_width}x{popup_height}+{center_x}+{center_y}')


        prompt_window.configure(bg="#f0f0f0")


        small_icon = Image.open("./Website/FileyFaceLogo.png")
        small_icon = small_icon.resize((32, 32), Image.Resampling.LANCZOS)
        small_icon_image = ImageTk.PhotoImage(small_icon)
        prompt_window.iconphoto(False, small_icon_image)

        tk.Label(prompt_window, text="Do you want to move:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)


        base_file_name = os.path.splitext(file_name)[0]
        file_extension = os.path.splitext(file_name)[1]


        input_frame_1 = tk.Frame(prompt_window, bg="#f0f0f0")
        input_frame_1.pack(pady=5)


        new_file_name_entry = tk.Entry(input_frame_1, font=("Arial", 12), width=30)
        new_file_name_entry.insert(0, base_file_name)
        new_file_name_entry.pack(side=tk.LEFT)
        

        extension_label = tk.Label(input_frame_1, text=file_extension, bg="#f0f0f0", font=("Arial", 12))
        extension_label.pack(side=tk.LEFT)

        tk.Label(prompt_window, text=f"to '{destination_folder}'?", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)

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
            user_choice[0] = None
            prompt_window.destroy()


        button_frame = tk.Frame(prompt_window, bg="#f0f0f0")
        button_frame.pack(pady=20)

        style = ttk.Style()

        style.configure("Rounded.TButton",
                        borderwidth=0,
                        relief="flat",
                        font=("Arial", 12),
                        padding=(10, 5))

        style.configure("Yes.TButton",
                        font=("Arial", 12),
                        background="#5cb85c",
                        foreground="black")
        style.map("Yes.TButton",
                background=[("active", "#3e8e41"),
                            ("pressed", "#2f6a2d")])

        style.configure("Regenerate.TButton",
                        font=("Arial", 12),
                        background="#ebc236",
                        foreground="black")
        style.map("Regenerate.TButton",
                background=[("active", "#c5a32f"),
                            ("pressed", "#b18e27")])

        style.configure("No.TButton",
                        font=("Arial", 12),
                        background="#f44336",
                        foreground="black")
        style.map("No.TButton",
                background=[("active", "#d32f2f"),
                            ("pressed", "#b71c1c")])

        yes_button = ttk.Button(button_frame, text="Yes", command=on_yes, style="Yes.TButton")
        yes_button.pack(side=tk.LEFT, padx=10)

        regen_button = ttk.Button(button_frame, text="Regenerate", command=on_regen, style="Regenerate.TButton")
        regen_button.pack(side=tk.LEFT, padx=10)

        no_button = ttk.Button(button_frame, text="No", command=on_no, style="No.TButton")
        no_button.pack(side=tk.RIGHT, padx=10)


        tk.Label(prompt_window, text=f"Add suggestions or desired file locations below:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
        
        input_frame_2 = tk.Frame(prompt_window, bg="#f0f0f0")
        input_frame_2.pack(pady=5)
        
        suggestions_entry = tk.Entry(input_frame_2, font=("Arial", 12), width=30)
        suggestions_entry.pack(side=tk.LEFT)

        user_choice = [None, None, None]

        prompt_window.protocol("WM_DELETE_WINDOW", prompt_window.destroy)
        prompt_window.mainloop()
        

        return user_choice

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
    