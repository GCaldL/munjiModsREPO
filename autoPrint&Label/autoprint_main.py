# imports
import printerManager
import folderMonitor
import labelMaker
import GUIs
import configManager

# consts
configINI = "/config.ini"

# init
config = configManager.get()

# main loop

while True:
    openDocs = folderMonitor.getCurrent()
