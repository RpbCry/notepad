import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import re

def new_file():
    text_area.delete("1.0", tk.END)
    root.title("Notepad")

def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
    if file_path:
        text_area.delete("1.0", tk.END)
        with open(file_path, "r") as file:
            text_area.insert(tk.END, file.read())
        root.title(f"Notepad - {file_path}")

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get("1.0", tk.END))
        root.title(f"Notepad - {file_path}")

def cut_text():
    text_area.event_generate("<<Cut>>")

def copy_text():
    text_area.event_generate("<<Copy>>")

def paste_text():
    text_area.event_generate("<<Paste>>")

def select_all():
    text_area.tag_add("sel", "1.0", "end")

def toggle_bold():
    current_tags = text_area.tag_names("sel.first")
    if "bold" in current_tags:
        text_area.tag_remove("bold", "sel.first", "sel.last")
    else:
        text_area.tag_add("bold", "sel.first", "sel.last")

def toggle_italic():
    current_tags = text_area.tag_names("sel.first")
    if "italic" in current_tags:
        text_area.tag_remove("italic", "sel.first", "sel.last")
    else:
        text_area.tag_add("italic", "sel.first", "sel.last")

def find_text():
    def find():
        search_text = find_entry.get()
        text_area.tag_remove("match", "1.0", tk.END)
        matches = 0
        if search_text:
            start_pos = "1.0"
            while True:
                start_pos = text_area.search(search_text, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(search_text)}c"
                text_area.tag_add("match", start_pos, end_pos)
                matches += 1
                start_pos = end_pos
            text_area.tag_config("match", background="yellow", foreground="black")
    
        find_status_label.config(text=f"{matches} matches found")

    find_dialog = tk.Toplevel(root)
    find_dialog.title("Find Text")
    find_dialog.geometry("300x100")
    find_label = tk.Label(find_dialog, text="Find:")
    find_label.pack(pady=5)
    find_entry = tk.Entry(find_dialog, width=30)
    find_entry.pack(pady=5)
    find_button = tk.Button(find_dialog, text="Find", command=find)
    find_button.pack(pady=5)
    find_status_label = tk.Label(find_dialog, text="")
    find_status_label.pack(pady=5)

root = tk.Tk()
root.title("Notepad")

text_area = tk.Text(root, wrap=tk.WORD)
text_area.pack(expand=tk.YES, fill=tk.BOTH)

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)

edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Paste", command=paste_text)
edit_menu.add_command(label="Select All", command=select_all)
edit_menu.add_separator()
edit_menu.add_command(label="Toggle Bold", command=toggle_bold)
edit_menu.add_command(label="Toggle Italic", command=toggle_italic)

search_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Search", menu=search_menu)
search_menu.add_command(label="Find", command=find_text)

root.mainloop()
