# imports
import printerManager
import labelMaker
import GUIs
import configManager
import logManager
import fileManager

# consts
CONFIG = "/config.ini"
LOG = "/log.json"

# ____path___________|_printed__|_labeled_|__found__|
# __labels.pdf_+ {___|______0___|__False__|__True___|
# _/labels/4215.pdf__|______0___|__False__|__True___|
# _/labels/4216.pdf__|______1___|__True___|__True___|
# _/labels/4217.pdf }|______3___|__True___|__True___|
# __4216.pdf_________|______1___|__True___|__True___|
# __4217.pdf_________|______3___|__True___|__False__|

# init
config = configManager.get(CONFIG)
# docs in folder that were already there
documents = logManager.readLog(LOG)
for doc in documents:
    if fileManager.isValidPath(config.root_folder + doc.path):
        doc.found = True
    else:
        doc.found = False


fileManager.initWatchDog(config.root_folder)

# main loop
while True:
    # Everything new that lands in the folder
    # everytime new files is called fileManager will clear it's new file buffer
    new_documents = fileManager.newFiles()
    # Everything that was in the folder before start??
    for doc in new_documents:
        if logManager.doesEntryExist(doc.path) == False:
            documents += logManager.newLogEntry(doc.path, 0, False, True)

    for doc in documents:
        if doc.labeled == False:
            labeledDOC = labelMaker.generateLabels(doc.path)
