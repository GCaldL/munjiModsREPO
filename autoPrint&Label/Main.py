import re
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from pypdf import PdfReader

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
import os

# My LIBS

import QRLABEL as qrlabelib
import PRINTERS as printlib


def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    print(filename)


def somfunc():
    print("I'm doing something lol")


root = Tk()
root.title("Auto Print")
# root.iconbitmap("munji.ico")
root.attributes('-topmost', True)

# settings
folder_path = StringVar()
folder_path.set("C:/Users/info/Downloads")

options = []
printers = printlib.getPrinters()
for printer in printers:
    options.append(printer[1].split(",")[0])

# UI
# Downloads Selector
path_label = Label(master=root, text="Path:")
path_label.grid(row=0, column=1)
path_label = Label(master=root, textvariable=folder_path, background="yellow")
path_label.grid(row=0, column=2)

path_selector = Button(text="Browse", command=browse_button)
path_selector.grid(row=0, column=3)

a4Set = StringVar()
a4Set.set("Choose Printer")
lbSet = StringVar()
lbSet.set("Choose Printer")

# Printer Selector
a4_label = Label(master=root, text="A4 Printer:")
a4_label.grid(row=1, column=1)
A4_printer = OptionMenu(root, a4Set, *options)
A4_printer.grid(row=1, column=3)

a4_label = Label(master=root, text="Label Printer:")
a4_label.grid(row=2, column=1)
A4_printer = OptionMenu(root, lbSet, *options)
A4_printer.grid(row=2, column=3)

# add QR Code to labels
makeqr = tk.IntVar()
makeqr.set(True)
makeqr_checkbox = Checkbutton(master=root, text='Add QR Code to Labels',
                              variable=makeqr, onvalue=True, offvalue=False)
makeqr_checkbox.grid(row=3, column=2)

# other settings lol
print_queue = []
# hotdog watchdog stuff
my_event_handler = PatternMatchingEventHandler(["*.pdf"], None, False, True)


def on_modified(event):
    print(f"{event.src_path} has been modified")
    if [event.src_path, False] in print_queue:
        doNULL = event.src_path
    else:
        time.sleep(0.5)
        print_queue.append([event.src_path, False])


my_event_handler.on_created = on_modified
my_event_handler.on_modified = on_modified

# OH GOD DON'T CHANGE THIS!!!
RECURSIVE = False
my_observer = Observer()
my_observer.schedule(my_event_handler, folder_path.get(), recursive=RECURSIVE)
my_observer.start()


while True:
    for doc in print_queue:
        # os.path.getmtime('C:/Users/info/Downloads/sample (2).pdf)
        if doc[1] == False and time.time() - os.path.getmtime(doc[0]) > 1:
            # print doc
            path = doc[0]
            print("printing doc:", path)
            # get doc size letter or a4
            pageSize = qrlabelib.getDocSize(path)
            if (pageSize == "LBL"):
                # add QR
                if makeqr.get():
                    generated_pdfs = qrlabelib.generateLabels(path)
                    # print
                    for file in generated_pdfs:
                        printlib.print_file(lbSet.get(), file)
                else:
                    printlib.print_file(lbSet.get(), path)
            else:
                printlib.print_file(a4Set.get(), path)
            # don't double print
            doc[1] = True
            # update GUI
    print(lbSet.get(), a4Set.get(), makeqr.get())
    root.update()
    time.sleep(0.1)
