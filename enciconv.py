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

        self.__input_filename = str()
        self.__input_set = False
        self.__output_filename = str()
        self.__output_set = False
        self.__subtitle_filename = str()
        self. __subtitle_set = False

    def create_frames(self):
        # Top level frame, hogy ossze pakoljak mindent.
        self.toplevel_frame = tk.Frame(self, bd=1)
        self.toplevel_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Elso frame az input fajloknak
        self.file_frame = tk.Frame(self.toplevel_frame, bd=1)
        self.file_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.file_frame.grid_columnconfigure(0, weight=1)

        # Masodik frame a gomboknak
        self.button_frame = tk.Frame(self.toplevel_frame, bd=1)
        self.button_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

    def create_widgets(self):
        # Input adatok
        self.input_file = tk.Label(self.file_frame,
                                   textvariable=self.input_filename,
                                   wraplength=130)
        self.input_file_button = tk.Button(self.file_frame, text="...",
                                           command=self.get_file)

        # Output adatok
        self.output_file = tk.Label(self.file_frame,
                                    textvariable=self.output_filename,
                                    wraplength=130)
        self.output_file_button = tk.Button(self.file_frame, text="...",
                                            command=self.save_file,
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
                                              command=self.get_sub,
                                              state=tk.DISABLED)

        # Feldolgozási gombok :)
        self.convert_button = tk.Button(self.button_frame, text="Konvertálás", command=self.convert, state=tk.DISABLED)
        self.quit = tk.Button(self.button_frame, text="Kilépés", command=self.winfo_toplevel().destroy)

    def pack_well(self):
        # Megjelenítés
        self.input_file.grid(row=0, column=0, sticky=(tk.W, tk.N, tk.S))
        self.input_file_button.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E))
        self.output_file.grid(row=1, column=0, sticky=(tk.W, tk.N, tk.S))
        self.output_file_button.grid(row=1, column=1, sticky=(tk.E, tk.N, tk.S))
        self.subtitle_checkbox.grid(row=2, column=0, sticky=(tk.N, tk.W, tk.S, tk.E), columnspan=2)
        self.subtitle_file.grid(row=3, column=0, sticky=(tk.W, tk.N, tk.S))
        self.subtitle_file_button.grid(row=3, column=1, sticky=(tk.E, tk.N, tk.S))
        self.convert_button.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.S))
        self.quit.grid(row=0, column=1, sticky=(tk.E, tk.S, tk.N))
        tk.Grid.columnconfigure(self.button_frame, 0, weight=1)

    def convert(self):
        if not self.input_set:
            messagebox.showerror("Hiba!", "Nem adtál meg bemeneti fájlt!")
        if not self.output_set:
            messagebox.showerror("Hiba!", "Nem adtál meg kimeneti fájlt!")
        if not self.subtitle_int.get():
            command = "mencoder -oac mp3lame -ovc xvid -xvidencopts pass=1 -o {1} {0}".format(
                self.inf, self.ouf
            )
        else:
            command = "mencoder -oac mp3lame -ovc xvid -xvidencopts pass=1 -sub {2} -o {1} {0}".format(
                self.inf, self.ouf, self.sfn
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

    def get_file(self):
        self.inf = filedialog.askopenfilename(
            initialdir=Application.user,
            title="Válaszd ki a fájlt!"
        )
        self.ouf = os.path.splitext(self.inf)[0] + '.avi'
        self.output_file_button.config(state="normal")
        self.convert_button.config(state="normal")
        self.master.update_idletasks()

    def save_file(self):
        _tmp = filedialog.asksaveasfilename(
                initialdir=Application.user,
                initialfile="{0}.{1}".format(os.path.splitext(
                    os.path.basename(self.input_filename.get()))[0], 'avi')
            )
        if os.path.isfile(_tmp):
            _res = messagebox.askyesno("Van ilyen fájl!", "Felülírjam? ({0})".format(_tmp))
            if _res:
                self.ouf = _tmp
                self.master.update_idletasks()
            else:
                self.save_file()

    def get_sub(self):
        self.sfn = filedialog.askopenfilename(
                initialdir=Application.user,
                title="Válaszd ki a feliratot!"
            )
        self.master.update_idletasks()

    def subtitle_checked(self):
        if self.subtitle_int.get():
            self.subtitle_file.config(state=tk.NORMAL)
            self.subtitle_file_button.config(state=tk.NORMAL)
        else:
            self.subtitle_file.config(state=tk.DISABLED)
            self.subtitle_file_button.config(state=tk.DISABLED)

    @property
    def inf(self):
        return self.__input_filename

    @inf.setter
    def inf(self, val):
        self.__input_filename = val
        self.input_filename.set(
            os.path.basename(val)
        )
        self.__input_set = True

    @property
    def ouf(self):
        return self.__output_filename

    @ouf.setter
    def ouf(self, fn):
        self.__output_filename = fn
        self.output_filename.set(
            os.path.basename(fn)
        )
        self.__output_set = True

    @property
    def sfn(self):
        return self.__subtitle_filename

    @sfn.setter
    def sfn(self, fn):
        self.subtitle_filename.set(
            os.path.basename(fn)
        )
        self.__subtitle_set = True

    @property
    def input_set(self):
        return self.__input_set

    @property
    def output_set(self):
        return self.__output_set

    @property
    def subtitle_set(self):
        return self.__subtitle_set

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
