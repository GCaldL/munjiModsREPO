import os
import win32print


def getPrinters():
    return win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)


def print_file(printer, file):
    os.system(
        """.\sumatra\SumatraPDF.exe -print-to "{}" "{}" """.format(printer, file))
