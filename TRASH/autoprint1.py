from pypdf import PdfReader
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import convert_shipping_labels as qrlabelib

import os
import win32print
from pypdf import PdfReader

print(win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1))

if __name__ == "__main__":
    my_event_handler = PatternMatchingEventHandler(
        ["*.pdf"], None, False, True)

print_queue = []

def getDocSize(path):
    reader = PdfReader(path)
    box = reader.pages[0].mediabox
    print(box)
    if box.width == 283.0 or box.width == 425.19999999999999:
        return "Office Label Printer (ZDes-GK420d)"
    else:
        return "A4 Office Printer (BrotherMFC-J6730DW)"


def on_modified(event):
    print(f"{event.src_path} has been modified")
    if [event.src_path, False] in print_queue:
        doNULL = event.src_path
    else:
        time.sleep(0.5)
        print_queue.append([event.src_path, False])


my_event_handler.on_created = on_modified
my_event_handler.on_modified = on_modified

PATH = "C:/Users/info/Downloads/"
RECURSIVE = True
my_observer = Observer()
my_observer.schedule(my_event_handler, PATH, recursive=RECURSIVE)
my_observer.start()

try:
    while True:
        time.sleep(1)
        for doc in print_queue:
            # os.path.getmtime('C:/Users/info/Downloads/sample (2).pdf)
            if doc[1] == False and time.time() - os.path.getmtime(doc[0]) > 1:
                # print doc
                path = doc[0]
                print("printing doc:", path)
                # get doc size letter or a4
                printername = getDocSize(path)
                if (printername == "Office Label Printer (ZDes-GK420d)"):
                    # add QR
                    qrlabelib.genNew(path)
                # print doc
                print("printing:" + path)
                os.system(
                    """.\sumatra\SumatraPDF.exe -print-to "{}" "{}" """.format(printername, path))
                # print("PDF printing took %5.9f seconds" % (end - start))
                # don't double print
                doc[1] = True
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()
