# Log Manager
import csv
from csv import DictReader


def readLog(path):
    with open(path, 'r') as f:
        dict_reader = DictReader(f)
        docs = list(dict_reader)
    print(docs)
    return docs


def writeLog(path, dictionary):
    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["path", "printed", "labeled", "found"])
        for data in dictionary:
            values = [data["path"], data["printed"],
                      data["labeled"], data["found"]]
            print(values)
            writer.writerow(values)
    return


def writeLogAppend(path, dictionary):
    with open(path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for data in dictionary:
            values = [data["path"], data["printed"],
                      data["labeled"], data["found"]]
            print(values)
            writer.writerow(values)
    return

new = readLog("log.csv")
