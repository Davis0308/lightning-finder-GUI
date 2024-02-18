import tkinter as tk
from subprocess import call
from tkinter import filedialog
from configparser import ConfigParser

rt = tk.Tk()
rt.geometry("500x300")
rt.title("lightning-finder GUI")
rt.iconbitmap("lightning-finder-GUI.ico")


#initializing configparser and defining config file
configini=ConfigParser(comment_prefixes='', allow_no_value=True)
configini.read('config.ini')

def main_run():
    loading_label = tk.Label(rt, text="Loading...")
    loading_label.grid(row=2, pady=10, padx=10)
    rt.update_idletasks()
    video_path_from_entry = video_path_entry.get()
    with open("config.ini", "w") as ow:
        configini.set("MainSettings", "video_file_path", video_path_from_entry)
        configini.write(ow)
    call(["python", "main.py"])
    print("Ran main script")
    loading_label.destroy()

def select_video():
    video_path = filedialog.askopenfilename()
    print(f"Video path: {video_path}")
    video_path_entry.delete(0, tk.END)
    video_path_entry.insert(0, video_path)
    return video_path


button_start = tk.Button(rt, text="start main", command=main_run)
button_start.grid(row=1, pady=10, padx=10)

video_path_label = tk.Label(rt, text="Video path").grid(row=0, column=1)
video_path_entry = tk.Entry(rt, width=60)
video_path_entry.grid(row=1, column=1)
save_button = tk.Button(rt, text="Browse", command=select_video).grid(row=1, column=2)



rt.mainloop()

