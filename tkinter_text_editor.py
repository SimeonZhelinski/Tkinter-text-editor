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
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        self.line_numbers_frame = tk.Frame(self.window)
        self.line_numbers_frame.grid(row=1, column=0, sticky="ns")

        self.text_area_frame = tk.Frame(self.window)
        self.text_area_frame.grid(row=1, column=1, sticky="nsew")

        self.scrollbar = tk.Scrollbar(self.text_area_frame, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.h_scrollbar = tk.Scrollbar(self.text_area_frame, orient=tk.HORIZONTAL)
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")

        self.text_area = tk.Text(self.text_area_frame, wrap=tk.NONE, font=('Century Gothic', 12),
                                 yscrollcommand=self.scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        self.text_area.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.scrollbar.config(command=self.text_area.yview)
        self.h_scrollbar.config(command=self.text_area.xview)

        self.text_area.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.text_area_frame.grid_rowconfigure(0, weight=1)
        self.text_area_frame.grid_columnconfigure(0, weight=1)

        self.line_numbers_canvas = tk.Canvas(self.line_numbers_frame, bg='lightgrey', width=40)
        self.line_numbers_canvas.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        self.line_numbers = tk.Label(self.line_numbers_frame, bg='lightgrey', fg='black', anchor='nw', justify='left')
        self.line_numbers_canvas.create_window((0, 0), window=self.line_numbers, anchor='nw')

        self.current_file = None

        frm_buttons = ttk.Labelframe(self.window, text=" Menu ", bootstyle=PRIMARY)
        frm_buttons.grid(row=0, column=0, columnspan=2, sticky="ew")

        btn_new = ttk.Button(frm_buttons, text="New", command=self.new_file, bootstyle=PRIMARY)
        btn_open = ttk.Button(frm_buttons, text="Open", command=self.open_file, bootstyle=PRIMARY)
        btn_save = ttk.Button(frm_buttons, text="Save", command=self.save_file, bootstyle=SUCCESS)
        btn_save_as = ttk.Button(frm_buttons, text="Save As...", command=self.save_as_file, bootstyle=SUCCESS)
        btn_exit = ttk.Button(frm_buttons, text="Exit", command=self.on_closing, bootstyle=DANGER)

        btn_new.grid(row=0, column=0, padx=5, pady=5)
        btn_open.grid(row=0, column=1, padx=5, pady=5)
        btn_save.grid(row=0, column=2, padx=5, pady=5)
        btn_save_as.grid(row=0, column=3, padx=5, pady=5)
        btn_exit.grid(row=0, column=5, padx=5, pady=5)

        frm_buttons.grid_columnconfigure(0, weight=0)
        frm_buttons.grid_columnconfigure(1, weight=0)
        frm_buttons.grid_columnconfigure(2, weight=0)
        frm_buttons.grid_columnconfigure(3, weight=0)
        frm_buttons.grid_columnconfigure(4, weight=1)
        frm_buttons.grid_columnconfigure(5, weight=0)

        self.text_area.bind('<KeyRelease>', self.update_line_numbers)
        self.text_area.bind('<MouseWheel>', self.update_line_numbers)
        self.text_area.bind('<Configure>', self.update_line_numbers)

        self.update_line_numbers()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_line_numbers(self, event=None):
        line_count = int(self.text_area.index('end-1c').split('.')[0])
        lines = "\n".join(str(i) for i in range(1, line_count + 1))

        if self.line_numbers['text'] != lines:
            self.line_numbers.config(text=lines, font=('Century Gothic', 12))

            self.line_numbers_frame.config(width=max(40, self.line_numbers.winfo_reqwidth()))

            self.line_numbers_canvas.configure(scrollregion=self.line_numbers_canvas.bbox("all"))

        self.align_line_numbers()

    def align_line_numbers(self, event=None):
        self.line_numbers_canvas.yview_moveto(self.text_area.yview()[0])

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
