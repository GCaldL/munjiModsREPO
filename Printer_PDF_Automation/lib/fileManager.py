import os
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


def isValidPath(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False


files = []


def on_modified(event):
    global files
    if event.src_path not in files:
        files += [event.src_path]


def initWatchDog(path):
    event_handler = PatternMatchingEventHandler(["*.pdf"], None, False, True)
    event_handler.on_created = on_modified
    event_handler.on_modified = on_modified

    my_observer = Observer()
    my_observer.schedule(event_handler, path, recursive=False)
    my_observer.start()


initWatchDog("C:/Users/info/Downloads")

while True:
    print(files)
