import os
import sqlite3
import shutil
import time

def get_web_history(file):
    time.sleep(0.3)
    history = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\History")
    history_copy = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\History_copy")
    shutil.copyfile(history, history_copy)
    conn = None

    try:
        conn = sqlite3.connect(history_copy)
        cursor = conn.cursor()
        query = f"SELECT id, target_path FROM downloads WHERE target_path LIKE '%{file}%'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            id, path = result
            query = f"SELECT url FROM downloads_url_chains WHERE id = {id}"
            cursor.execute(query)
            url = cursor.fetchone()

            if url:
                url = url[0]
                #print(f"{url}")
                return f"{url}"
            else:
                #print("NOOOIIIII")
                return None
            
        else:
            #print("NOOOOO")
            return None
    
    except sqlite3.Error as e:
        return None
    
    finally:
        if conn:
            conn.close()