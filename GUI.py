import tkinter as tk
from subprocess import call
from tkinter import filedialog
from configparser import ConfigParser
from tkinter import ttk
import os
import validators

#initializing tkinter root window
rt = tk.Tk()
rt.geometry("700x400")
rt.minsize(700, 400)
rt.title("lightning-finder GUI")
rt.iconbitmap("lightning-finder-GUI.ico")

#initializing ttk notebook for tabs
nb = ttk.Notebook(rt)
nb.pack(expand = True, fill="both", pady=(5,0))

#creating tabs
main_tab = tk.Frame(nb)
settings_tab = tk.Frame(nb)
nb.add(main_tab, text="Main")
nb.add(settings_tab, text="Settings")

#making labelframes
#main tab
path_lblframe = tk.LabelFrame(main_tab, text="Path")
path_lblframe.grid(row=0, column=0, columnspan=3, sticky="swen", padx=5, pady=2)
#settings tab
bool_int_settings_lblframe = tk.LabelFrame(settings_tab, text="intbool")
bool_int_settings_lblframe.grid(row=0, column=0, sticky="swen", columnspan=2, padx=5, pady=2)
str_int_settings_lblframe = tk.LabelFrame(settings_tab, text="str")
str_int_settings_lblframe.grid(row=0, column=2, sticky="swen", columnspan=2, padx=5, pady=2)


#configuring grids
main_tab.rowconfigure((0,1,2), weight= 1, uniform="a")
main_tab.columnconfigure((0,1,2), weight= 1, uniform="a")
settings_tab.rowconfigure((0,1,2,3), weight= 1, uniform="a")
settings_tab.columnconfigure((0,1,2,3), weight= 1, uniform="a")
path_lblframe.rowconfigure((0,1,2), weight= 1, uniform="a")
path_lblframe.columnconfigure(0, weight=2, uniform="a")
path_lblframe.columnconfigure(1, weight=3, uniform="a")
path_lblframe.columnconfigure(2, weight=1, uniform="a")


#initializing configparser and defining config file
configini = ConfigParser(comment_prefixes='', allow_no_value = True)
configini.read('config.ini')

    
def main_run(_=None): #using _=None as parameter because .bind() returns an argument and idk how to prevent it
    video_path_from_entry = video_path_entry.get()
    if os.path.exists(video_path_from_entry) is True or validators.url(video_path_from_entry) is True:
        loading_label = tk.Label(rt, text="Loading...")
        loading_label.pack(side="bottom", fill="x")
        button_start.config(text="START")
        rt.update() #should use rt.update_idletasks() but that glitches out for now, change later
        with open("config.ini", "w") as ow:
            configini.set("MainSettings", "video_file_path", video_path_from_entry)
            configini.write(ow)
        call(["python", "main.py"])
        print("Ran main script")
        loading_label.pack_forget()
    else:
        print("Failed: Broken path")
        button_start.config(text="START\nErr: Broken path/link")
        return 0


#function to ask for video path
def select_video():
    video_path = filedialog.askopenfilename()
    if len(video_path) != 0:
        print(f"Video path: {video_path}")
        video_path_entry.delete(0, tk.END)
        video_path_entry.insert(0, video_path)
        return video_path

#making label+entry+button for video path
video_path_label = tk.Label(path_lblframe, text="Video path (or link, experimental)")
video_path_label.grid(row=0, column=0, sticky="e")

video_path_entry = tk.Entry(path_lblframe)
video_path_entry.insert(0, configini.get("MainSettings", "video_file_path"))
video_path_entry.grid(row=0, column=1, sticky="we")

video_path_browse_button = tk.Button(path_lblframe, text="Browse", command=select_video)
video_path_browse_button.grid(row=0, column=2, padx=5, sticky="w")

#making settings save and reset default buttons
settings_save_button = tk.Button(settings_tab, text="Save", command=None, width=20)
settings_restore_button = tk.Button(settings_tab, text="Restore", command=None, width=20)
settings_save_button.grid(row=3, column=2, sticky="se", pady=5)
settings_restore_button.grid(row=3, column=3, sticky="sw", pady=5)

#making settings checkboxes
delete_proc_dir_when_done_checkbox_state = tk.BooleanVar()
delete_proc_dir_when_done_checkbox = tk.Checkbutton(bool_int_settings_lblframe, text="Delete processing dir when done", var=delete_proc_dir_when_done_checkbox_state)
delete_proc_dir_when_done_checkbox.pack()

tempcheck1_state = tk.BooleanVar()
tempcheck1 = tk.Checkbutton(bool_int_settings_lblframe, text="make this a drop down menu and add ints", var=delete_proc_dir_when_done_checkbox_state)
tempcheck1.pack()

#start button
button_start = tk.Button(main_tab, text="START", command=main_run, background="#de5454")
button_start.grid(row=2, column=2, pady=10, padx=10, sticky="se", ipadx=20, ipady=15)
video_path_entry.bind("<Return>", func=main_run)




temp_button_to_resize_to_default = tk.Button(main_tab, text="default size - temp", command=lambda: rt.geometry("700x400"))
#temp_button_to_resize_to_default.grid(row=2, column=0, sticky="sw")



rt.mainloop()

