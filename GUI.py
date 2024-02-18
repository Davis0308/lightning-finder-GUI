import tkinter as tk
from subprocess import call
import config
import time

rt = tk.Tk()
rt.geometry("300x300")

runTrigger = 0

def main_run():
    loadingLabel = tk.Label(rt, text="Loading...")
    loadingLabel.grid(row=2, pady=10, padx=10)
    rt.update_idletasks()
    call(["python", "main.py"])
    print("Ran main script")
    loadingLabel.destroy()

def configEdit():
    config.MainSettings.proc_dir_name = config_entry.get()
    print(f"changed to {config_entry.get()}")



button_start = tk.Button(rt, text="start main", command=main_run)
button_start.grid(row=1, pady=10, padx=10)

config_label = tk.Label(rt, text="proc_dir_name").grid(row=0, column=1)
config_entry = tk.Entry(rt)
config_entry.grid(row=1, column=1)
save_button = tk.Button(rt, text="Save", command=configEdit).grid(row=1, column=2)

config.MainSettings.proc_dir_name



rt.mainloop()

