#!/usr/bin/env python3
# -*- coding:iso-8859-2 -*-

import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog


class Application(tk.Frame):
    user = os.path.expanduser('~')

    def __init__(self, master=None):
        self.master = master
        super().__init__(self.master)
        self.winfo_toplevel().title("Enciconv <3")
        self.winfo_toplevel().geometry("170x170")
        self.pack()

        self.input_filename = tk.StringVar(self)
        self.input_filename.set("Bemeneti fájlnév")
        self.output_filename = tk.StringVar(self)
        self.output_filename.set("Kimeneti fájlnév")
        self.subtitle_int = tk.IntVar()
        self.subtitle_filename = tk.StringVar(self)
        self.subtitle_filename.set("Felirat fajnev")
        self.create_frames()

        self.create_widgets()
        self.pack_well()

    def create_frames(self):
        self.file_frame = tk.Frame(self, bd=1, bg="yellow")
        self.file_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.button_frame = tk.Frame(self, bd=1, bg="red")
        self.button_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

    def create_widgets(self):
        # Input adatok
        self.input_file = tk.Label(self.file_frame,
                                   textvariable=self.input_filename,
                                   wraplength=130)
        self.input_file_button = tk.Button(self.file_frame, text="...",
                                           command=lambda: self.get_file(self.input_filename))

        # Output adatok
        self.output_file = tk.Label(self.file_frame,
                                    textvariable=self.output_filename,
                                    wraplength=130)
        self.output_file_button = tk.Button(self.file_frame, text="...",
                                            command=lambda: self.save_file(self.output_filename),
                                            state=tk.DISABLED)
        # Feliratok hozzaadasa
        self.subtitle_checkbox = tk.Checkbutton(self.file_frame,
                                                text="Felirat",
                                                variable=self.subtitle_int,
                                                command=self.subtitle_checked)
        self.subtitle_file = tk.Label(self.file_frame,
                                      textvariable=self.subtitle_filename,
                                      wraplength=130,
                                      state=tk.DISABLED)
        self.subtitle_file_button = tk.Button(self.file_frame, text="...",
                                              command=lambda: self.get_file(self.subtitle_filename),
                                              state=tk.DISABLED)

        # Feldolgozási gombok :)
        self.convert_button = tk.Button(self.button_frame, text="Konvertálás", command=self.convert, state=tk.DISABLED)
        self.quit = tk.Button(self.button_frame, text="Kilépés", command=self.winfo_toplevel().destroy)

    def pack_well(self):
        # Megjelenítés
        self.input_file.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.input_file_button.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.output_file.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.output_file_button.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.subtitle_checkbox.grid(row=2, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.subtitle_file.grid(row=3, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.subtitle_file_button.grid(row=3, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.convert_button.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.quit.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        tk.Grid.columnconfigure(self.button_frame, 0, weight=1)

    def convert(self):
        command = "mencoder -oac mp3lame -ovc xvid -xvidencopts pass=1 -o {1} {0}".format(
            self.input_filename.get(),
            self.output_filename.get()
        )
        process = subprocess.Popen(command.split(),
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        error = stderr.decode()
        if error:
            self.mess = messagebox.showerror("Sikertelen", "{0}: {1}".format(self.input_filename.get(), error))
        self.mess = messagebox.showinfo("Sikeres", "Kész: {0}".format(self.output_filename.get()))

    def get_file(self, var):
        var.set(
            filedialog.askopenfilename(
                initialdir=Application.user,
                title="Válaszd ki a fájlt!"
            )
        )
        print(var.get())
        self.output_filename.set("{0}.{1}".format(
            os.path.splitext(var.get())[0], 'avi'))
        self.output_file_button.config(state="normal")
        self.convert_button.config(state="normal")
        self.master.update_idletasks()

    def save_file(self, var):
        var.set(
            filedialog.asksaveasfilename(
                initialdir=Application.user,
                initialfile="{0}.{1}".format(os.path.splitext(
                    os.path.basename(self.input_filename.get()))[0], 'avi')
            )
        )
        self.convert_button.config(state="normal")
        self.master.update_idletasks()

    def subtitle_checked(self):
        if self.subtitle_int.get():
            self.subtitle_file.config(state=tk.NORMAL)
            self.subtitle_file_button.config(state=tk.NORMAL)
        else:
            self.subtitle_file.config(state=tk.DISABLED)
            self.subtitle_file_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
