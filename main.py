import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

CONFIG_FILE = "programs.txt"

def load_programs():
    if not os.path.exists(CONFIG_FILE):
        return []
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def save_programs(program_list):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        for p in program_list:
            f.write(p + "\n")

def start_programs():
    programs = load_programs()
    if not programs:
        messagebox.showwarning("No Programs", "No programs configured!")
        return

    for program in programs:
        try:
            # --- BAT file requires shell=True ---
            if program.lower().endswith(".bat"):
                subprocess.Popen(program, shell=True)
            else:
                subprocess.Popen(program)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open:\n{program}\n\n{e}")

    messagebox.showinfo("Started", "All programs launched!")

def open_edit_window():
    edit_win = tk.Toplevel(root)
    edit_win.title("Edit Programs to Run")
    edit_win.geometry("500x400")

    program_list = load_programs()

    listbox = tk.Listbox(edit_win, font=("Arial", 12))
    listbox.pack(fill="both", expand=True, padx=10, pady=10)

    for item in program_list:
        listbox.insert("end", item)

    def add_program():
        file = filedialog.askopenfilename()
        if file:
            listbox.insert("end", file)

    def remove_selected():
        selection = listbox.curselection()
        if selection:
            listbox.delete(selection[0])

    def save_and_close():
        new_list = list(listbox.get(0, "end"))
        save_programs(new_list)
        edit_win.destroy()

    btn_frame = tk.Frame(edit_win)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Add Program", command=add_program, width=12).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Remove", command=remove_selected, width=12).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Save & Close", command=save_and_close, width=12).grid(row=0, column=2, padx=5)

root = tk.Tk()
root.title("One-Click Server Starter")
root.geometry("500x400")

menubar = tk.Menu(root)
submenu = tk.Menu(menubar, tearoff=0)
submenu.add_command(label="Edit Programs...", command=open_edit_window)
submenu.add_separator()
submenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Menu", menu=submenu)
root.config(menu=menubar)

start_btn = tk.Button(
    root,
    text="START SERVER",
    font=("Arial", 36, "bold"),
    bg="#4CAF50",
    fg="white",
    height=2,
    width=12,
    command=start_programs
)
start_btn.pack(expand=True)

root.mainloop()
