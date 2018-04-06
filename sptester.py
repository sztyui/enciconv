# -*- coding=iso-8859-2 -*-
import os
import sys
import time
import pathlib
import subprocess

import tkinter as tk

root = tk.Tk()


home = pathlib.Path.home()
command = "ls -ltrh {0}".format(
    os.path.join(home, "Letöltések/download/")
)
process = subprocess.Popen(command.split(),
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           universal_newlines=True
                           )

content = tk.StringVar(root)
content.set('~/')
textbox = tk.Label(root, textvariable=content,
                   width=70, background="black", fg="green", anchor='w')
textbox.pack()

for stdout_line in iter(process.stdout.readline, ""):
    content.set(stdout_line)
    root.update_idletasks()
    time.sleep(1)
process.stdout.close()

root.mainloop()
# for stdout_line in iter(process.stdout.readline, ""):
#     print(stdout_line)
#
# process.stdout.close()
# return_code = process.wait()
# if return_code:
#     print("Valami szar: {0}".format(return_code))
#
