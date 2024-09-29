import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class TextEditor:
    def __init__(self, window):

        ttk.Style().theme_use('darkly')
        self.window = window
        self.window.title("Text Editor")
        self.window.rowconfigure(1, minsize=500, weight=1)
        self.window.columnconfigure(0, minsize=900, weight=1)

        self.line_numbers_frame = tk.Frame(self.window)
        self.line_numbers_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.text_area_frame = tk.Frame(self.window)
        self.text_area_frame.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.text_area_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area = tk.Text(self.window, wrap=tk.WORD, font=('Century Gothic', 12))
        self.text_area.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)

        self.scrollbar.config(command=self.text_area.yview)

        self.line_numbers_canvas = tk.Canvas(self.line_numbers_frame, bg='lightgrey', width=40)
        self.line_numbers_canvas.pack(fill=tk.Y)

        self.line_numbers = tk.Label(self.line_numbers_frame, bg='lightgrey', fg='black', anchor='nw', justify='left')
        self.line_numbers_canvas.create_window((0, 0), window=self.line_numbers, anchor='nw')

        self.current_file = None

        frm_buttons = ttk.Labelframe(window, text=" Menu ", bootstyle=PRIMARY)
        frm_buttons.pack(side=tk.TOP, fill=tk.X)

        btn_new = ttk.Button(frm_buttons, text="New", command=self.new_file, bootstyle=DANGER)
        btn_open = ttk.Button(frm_buttons, text="Open", command=self.open_file, bootstyle=PRIMARY)
        btn_save = ttk.Button(frm_buttons, text="Save", command=self.save_file, bootstyle=SUCCESS)
        btn_save_as = ttk.Button(frm_buttons, text="Save As...", command=self.save_as_file, bootstyle=INFO)

        btn_new.pack(side=tk.LEFT, padx=5, pady=5)
        btn_open.pack(side=tk.LEFT, padx=5, pady=5)
        btn_save.pack(side=tk.LEFT, padx=5, pady=5)
        btn_save_as.pack(side=tk.LEFT, padx=5, pady=5)

        self.text_area.bind('<KeyRelease>', self.update_line_numbers)
        self.text_area.bind('<Configure>', self.update_line_numbers)

        self.update_line_numbers()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_line_numbers(self, event=None):
        line_count = int(self.text_area.index('end-1c').split('.')[0])
        lines = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.config(text=lines)

        self.line_numbers_frame.config(width=max(40, self.line_numbers.winfo_reqwidth()))
        self.line_numbers_canvas.configure(scrollregion=self.line_numbers_canvas.bbox("all"))

    def new_file(self):
        if self.text_area.edit_modified():
            answer = messagebox.askyesno("Save Current File",
                                         "Do you want to save the current file before creating a new one?")
            if answer:
                self.save_file()

        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.window.title("New File - Text Editor")
        self.text_area.edit_modified(False)
        self.update_line_numbers()

    def open_file(self):
        if self.text_area.edit_modified():
            answer = messagebox.askyesno("Save Current File",
                                         "Do you want to save the current file before opening a new one?")
            if answer:
                self.save_file()

        filepath = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if not filepath:
            return
        self.text_area.delete("1.0", tk.END)
        with open(filepath, mode="r", encoding="utf-8") as input_file:
            text = input_file.read()
            self.text_area.insert(tk.END, text)
        self.current_file = filepath
        self.window.title(f"Text Editor - {filepath}")
        self.text_area.edit_modified(False)
        self.update_line_numbers()

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.window.title(f"{self.current_file} - Text Editor")
            self.text_area.edit_modified(False)
        else:
            self.save_as_file()

    def save_as_file(self):
        filepath = asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, mode="w", encoding="utf-8") as output_file:
            text = self.text_area.get("1.0", tk.END)
            output_file.write(text)
        self.window.title(f"Text Editor - {filepath}")
        self.text_area.edit_modified(False)
        self.update_line_numbers()

    def on_closing(self):
        if self.text_area.edit_modified():
            answer = messagebox.askyesno("Quit", "Do you want to save the changes before exiting?")
            if answer:
                self.save_file()
        self.window.destroy()


if __name__ == "__main__":
    window = tk.Tk()
    app = TextEditor(window)
    window.mainloop()
