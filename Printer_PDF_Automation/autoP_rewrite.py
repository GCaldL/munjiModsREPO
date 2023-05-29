# imports
import configparser
import lib.logManager as logM
import lib.printerManager
import lib.labelMaker
import lib.fileManager
import lib.GUIs

# consts
CONFIG = "/config.ini"
# a4_printer = "A4 Office Printer (BrotherMFC-J6730DW)"
# label_printer = "Office Label Printer (ZDes-GK420d)"
# root_folder = "C:/Users/info/Downloads"

LOG = "/log.json"
# ____path___________|_printed__|_labeled_|__found__|
# __labels.pdf_+ {___|______0___|__False__|__True___|
# _/labels/4215.pdf__|______0___|__False__|__True___|
# _/labels/4216.pdf__|______1___|__True___|__True___|
# _/labels/4217.pdf }|______3___|__True___|__True___|
# __4216.pdf_________|______1___|__True___|__True___|
# __4217.pdf_________|______3___|__True___|__False__|

# init
config = configparser.ConfigParser()
config.read(CONFIG)
printers = [config["a4_printer"], config["label_printer"]]
root_folder = config["root_folder"]

# docs in folder that were already there
documents = logM.readLog(LOG)
for doc in documents:
    if fileManager.isValidPath(config.root_folder + doc.path):
        doc[3] = True
    else:
        doc[3] = False


fileManager.initWatchDog(config.root_folder)

# main loop
while True:
    # Everything new that lands in the folder
    # everytime new files is called fileManager will clear it's new file buffer
    new_documents = fileManager.newFiles()
    # Everything that was in the folder before start??
    for doc in new_documents:
        if logManager.doesEntryExist(doc.path) is False:
            documents += logManager.newLogEntry(doc.path, 0, False, True)

    for doc in documents:
        if doc.labeled is False:
            labeledDOC = labelMaker.generateLabels(doc.path)
