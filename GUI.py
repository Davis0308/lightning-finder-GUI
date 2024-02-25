import tkinter as tk
from subprocess import call
from tkinter import filedialog, ttk, messagebox
from configparser import ConfigParser
import os
import validators
import webbrowser

#initializing tkinter root window
rt = tk.Tk()
rt.geometry("750x450")
rt.minsize(750, 450)
rt.title("lightning-finder GUI")
rt.iconbitmap("lightning-finder-GUI.ico")

#initializing ttk notebook for tabs
nb = ttk.Notebook(rt)
nb.pack(expand = True, fill="both", pady=(5,0))

#initializing configparser and defining config file
configini=ConfigParser(comment_prefixes='', allow_no_value=True)
configini.read('config.ini')

#creating tabs
main_tab = ttk.Frame(nb)
settings_tab = ttk.Frame(nb)
about_tab = ttk.Frame(nb)
nb.add(main_tab, text="Main")
nb.add(settings_tab, text="Settings")
nb.add(about_tab, text="About")

#making labelframes
#main tab
path_lblframe = ttk.LabelFrame(main_tab, text="Path")
path_lblframe.grid(row=0, column=0, columnspan=3, sticky="swen", padx=5, pady=2)
#settings tab
bool_int_settings_lblframe = ttk.LabelFrame(settings_tab, text="1")
bool_int_settings_lblframe.grid(row=0, column=0, sticky="swen", columnspan=3, rowspan=2, padx=5, pady=2)
str_int_settings_lblframe = ttk.LabelFrame(settings_tab, text="2")
str_int_settings_lblframe.grid(row=0, column=3, sticky="swen", columnspan=3, rowspan=2, padx=5, pady=2)


#configuring grids
main_tab.rowconfigure((0,1,2), weight= 1)
main_tab.columnconfigure((0,1,2), weight= 1)
settings_tab.rowconfigure((0,1,2,3,4,5), weight= 1, uniform="b")
settings_tab.columnconfigure((0,1,2,3,4,5), weight= 1, uniform="b")
path_lblframe.rowconfigure((0,1,2), weight= 1, uniform="a")
path_lblframe.columnconfigure(0, weight=2, uniform="a")
path_lblframe.columnconfigure(1, weight=3, uniform="a")
path_lblframe.columnconfigure(2, weight=1, uniform="a")
bool_int_settings_lblframe.rowconfigure((0,1,2), weight=1)
bool_int_settings_lblframe.columnconfigure((0,1), weight=1)
str_int_settings_lblframe.rowconfigure((0,1), weight=1)
str_int_settings_lblframe.columnconfigure((0,1,2,3), weight=1)


#initializing configparser and defining config file
configini = ConfigParser(comment_prefixes='', allow_no_value = True)
configini.read('config.ini')

#making settings list(s)
average_brightness_algorithm_list = [0,1,2,3,4,5,6]

    
#function to start the main script
def main_run(_=None): #using _=None as parameter because .bind() returns an argument and idk how to prevent it
    video_path_from_entry = video_path_entry.get()
    if os.path.exists(video_path_from_entry) is True or validators.url(video_path_from_entry) is True:
        loading_label = ttk.Label(rt, text="Loading...")
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
        messagebox.showwarning("Error", "Broken path/link")
        return 0


#function to ask for video path
def select_video():
    video_path = filedialog.askopenfilename()
    if len(video_path) != 0:
        print(f"Video path: {video_path}")
        video_path_entry.delete(0, tk.END)
        video_path_entry.insert(0, video_path)
        return video_path


#function to update widthxheight entry fields with checkbox
def update_wxh_entries_from_checkbox():
    if custom_frameres_chcekbox_state.get() is False:
        custom_frameres_entry_width.delete(0, tk.END)
        custom_frameres_entry_height.delete(0, tk.END)
        custom_frameres_entry_width.config(state="disabled")
        custom_frameres_entry_height.config(state="disabled")

    else:
        configini.read('config.ini')
        resolution = configini.get("MainSettings", "frame_res")
        width, height = map(int, resolution.split('x'))
        custom_frameres_entry_width.config(state="enabled")
        custom_frameres_entry_height.config(state="enabled")
        custom_frameres_entry_width.insert(0, width)
        custom_frameres_entry_height.insert(0, height)


#function to update config.ini with updated settings
def update_configini_from_save_button():
    with open("config.ini", "w") as ow:
        configini.set("MainSettings", "proc_dir_name", str(proc_dir_name_entry.get()))
        configini.set("MainSettings", "delete_proc_dir_when_done", str(delete_proc_dir_when_done_checkbox_state.get()))
        configini.set("MainSettings", "custom_frameres", str(custom_frameres_chcekbox_state.get()))
        combined_resolution = f"{custom_frameres_entry_width.get()}x{custom_frameres_entry_height.get()}"
        if custom_frameres_chcekbox_state.get() is True:
            configini.set("MainSettings", "frame_res", combined_resolution)
        configini.set("MainSettings", "average_brightness_algorithm", str(average_brightness_algorithm_combobox.get()))
        configini.set("MainSettings", "number_of_labels_in_plot", str(number_of_labels_in_plot_spinbox.get()))
        configini.write(ow)
    print("Saved!")
    messagebox.showinfo("Info", "Settings have been saved.")

#function to restore default settings
def restore_default_configini():
    with open("config.ini", "w") as ow:
        configini.set("MainSettings", "proc_dir_name", "processing")
        configini.set("MainSettings", "delete_proc_dir_when_done", "True")
        configini.set("MainSettings", "custom_frameres", "False")
        configini.set("MainSettings", "frame_res", "64x36")
        configini.set("MainSettings", "average_brightness_algorithm", "2")
        configini.set("MainSettings", "number_of_labels_in_plot", "20")
        configini.set("MainSettings", "video_file_path", "")
        configini.write(ow)
        update_settings_shown()
        print("Restored!")
        messagebox.showinfo("Info", "Settings have been restored.")


#function to update all settings shown
def update_settings_shown():
    configini.read('config.ini')
    proc_dir_name_entry.delete(0, tk.END)
    proc_dir_name_entry.insert(0, configini.get("MainSettings", "proc_dir_name"))
    delete_proc_dir_when_done_checkbox_state.set(configini.getboolean("MainSettings", "delete_proc_dir_when_done"))
    custom_frameres_chcekbox_state.set(configini.getboolean("MainSettings", "custom_frameres"))
    update_wxh_entries_from_checkbox()
    average_brightness_algorithm_combobox.current(configini.getint("MainSettings", "average_brightness_algorithm"))
    number_of_labels_in_plot_spinbox_intvar.set(configini.getint("MainSettings", "number_of_labels_in_plot"))



### MAIN TAB
    
## Path frame
#making label+entry+button for video path
video_path_label = ttk.Label(path_lblframe, text="Video path (or link, experimental) ")
video_path_label.grid(row=1, column=0, sticky="e")

video_path_entry = ttk.Entry(path_lblframe)
video_path_entry.insert(0, configini.get("MainSettings", "video_file_path"))
video_path_entry.grid(row=1, column=1, padx=5, sticky="we")

video_path_browse_button = ttk.Button(path_lblframe, text="Browse", command=select_video)
video_path_browse_button.grid(row=1, column=2, sticky="w")

## Main tab
#start button
button_start = tk.Button(main_tab, text="START", command=main_run, background="#de5454")
button_start.grid(row=2, column=2, pady=10, padx=10, sticky="se", ipadx=20, ipady=15)
video_path_entry.bind("<Return>", func=main_run)



### SETTINGS TAB

##intbool frame
#making intbool widgets
delete_proc_dir_when_done_checkbox_state = tk.BooleanVar(value=configini.getboolean("MainSettings", "delete_proc_dir_when_done"))
delete_proc_dir_when_done_checkbox = ttk.Checkbutton(bool_int_settings_lblframe, text="Delete processing dir when done ", var=delete_proc_dir_when_done_checkbox_state)
delete_proc_dir_when_done_checkbox.grid(row=0, column=0, columnspan=2)
delete_proc_dir_when_done_checkbox

average_brightness_algorithm_combobox_strvar = tk.StringVar()
average_brightness_algorithm_combobox_label = ttk.Label(bool_int_settings_lblframe, text="Processing algorithm ")
average_brightness_algorithm_combobox_label.grid(row=1, column=0, sticky="e")
average_brightness_algorithm_combobox = ttk.Combobox(bool_int_settings_lblframe, values=average_brightness_algorithm_list, state="readonly", textvariable=average_brightness_algorithm_combobox_strvar)
average_brightness_algorithm_combobox.grid(row=1, column=1, sticky="w")
average_brightness_algorithm_combobox.current(configini.getint("MainSettings", "average_brightness_algorithm"))

number_of_labels_in_plot_spinbox_intvar = tk.IntVar(value=configini.getint("MainSettings", "number_of_labels_in_plot"))
number_of_labels_in_plot_spinbox_label = ttk.Label(bool_int_settings_lblframe, text="Numbers of labels in plot ")
number_of_labels_in_plot_spinbox_label.grid(row=2, column=0, sticky="e")
number_of_labels_in_plot_spinbox = ttk.Spinbox(bool_int_settings_lblframe, from_=0, to=100, textvariable=number_of_labels_in_plot_spinbox_intvar)
number_of_labels_in_plot_spinbox.grid(row=2, column=1, sticky="w")


##str frame
proc_dir_name_label = ttk.Label(str_int_settings_lblframe, text="Name of processing directory ")
proc_dir_name_label.grid(row=0, column=0, sticky="e")
proc_dir_name_entry = ttk.Entry(str_int_settings_lblframe)
proc_dir_name_entry.grid(row=0, column=1, columnspan=3, sticky="ew", padx=(2,50))
proc_dir_name_entry.insert(0, configini.get("MainSettings", "proc_dir_name"))


custom_frameres_chcekbox_state = tk.BooleanVar(value=configini.getboolean("MainSettings", "custom_frameres"))
custom_frameres_checkbox = ttk.Checkbutton(str_int_settings_lblframe, text="Custom processing resolution ", variable=custom_frameres_chcekbox_state, command=update_wxh_entries_from_checkbox)
custom_frameres_checkbox.grid(row=1, column=0, sticky="e", padx=5)



custom_frameres_entry_width = ttk.Entry(str_int_settings_lblframe, width=10)
custom_frameres_entry_width.grid(row=1, column=1, sticky="e")
custom_frameres_entry_x_label = ttk.Label(str_int_settings_lblframe, text="x")
custom_frameres_entry_x_label.grid(row=1, column=2)
custom_frameres_entry_height = ttk.Entry(str_int_settings_lblframe, width=10)
custom_frameres_entry_height.grid(row=1, column=3, sticky="w")

if custom_frameres_chcekbox_state.get() is False:
    custom_frameres_entry_width.config(state="disabled")
    custom_frameres_entry_height.config(state="disabled")
else:
        configini.read('config.ini')
        resolution = configini.get("MainSettings", "frame_res")
        width, height = map(int, resolution.split('x'))
        custom_frameres_entry_width.insert(0, width)
        custom_frameres_entry_height.insert(0, height)


#making settings save and reset default buttons
settings_save_button = ttk.Button(settings_tab, text="Save", command=update_configini_from_save_button, width=20)
settings_restore_button = ttk.Button(settings_tab, text="Restore", command=restore_default_configini, width=20)
settings_save_button.grid(row=5, column=4, sticky="se", pady=5)
settings_restore_button.grid(row=5, column=5, sticky="sw", pady=5)



### ABOUT TAB
github_project_url = "https://github.com/Davis0308/lightning-finder-GUI" 
about_label = ttk.Label(about_tab, text="lightning-finder GUI by Davis Schina\nV1.0.0 released 2024/02/25", font=("", 24), justify="center")
about_label.place(relx=0.5, rely=0.3, anchor="center")
about_link_label = ttk.Label(about_tab, text=github_project_url, font=("", 20), cursor="hand2", foreground="#0000EE")
about_link_label.place(relx=0.5, rely=0.7, anchor="center")
about_link_label.bind("<Button-1>", lambda _: webbrowser.open_new_tab(github_project_url))


#temp
# temp_button_to_resize_to_default = ttk.Button(main_tab, text="default size - temp", command=lambda: rt.geometry("750x450"))
# temp_button_to_resize_to_default.grid(row=2, column=0, sticky="sw")



rt.mainloop()

