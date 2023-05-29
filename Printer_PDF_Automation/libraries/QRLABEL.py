import os
from PIL import Image as pillow
import PyPDF2
from PyPDF2 import PdfReader
import fitz
import qrcode
import re


def getDocSize(path):
    reader = PdfReader(path)
    box = reader.pages[0].mediabox
    print(box)
    if box.width < 460:
        return "LBL"
    else:
        return "A4P"


def get_file_name(path):
    """Extract the base name of the file from the path."""
    return os.path.basename(path)


def generateLabels(path):
    # ARRAY OF PATHS TO NEW PDFS WITH QR CODES
    new_files = []
    rootfolder = os.path.dirname(path)
    # BCAUSE WE'RE USING TWO LIBS TO OPEN THE DOCUMENT WE'LL FIRST GET AND SAVE THE ORDER NOs AS ARRAY
    order_numbers = []
    # IF THERE IS NO REF ON THE FILE THEN THEY'LL BE PLAIN LABELS AND WE'LL USE THE FILE NAME :(
    document_name = get_file_name(path).split(".")[0]

    with open(path, "rb") as doc:
        pdf = PdfReader(doc)
        num_pages = len(pdf.pages)

        for page_number in range(num_pages):
            page = pdf.pages[page_number]
            text = page.extract_text()
            match = re.search(r'Ref1: (\d+)', text)
            if match:
                order_number = match.group(1)
                print(f"Order number on page {page_number}: {order_number}")
                order_numbers += [order_number]
            else:
                print(f"No order number found on page {page_number}")
                order_numbers += [document_name]
        print(order_numbers)

    document = fitz.open(path)
    for page in document:
        zoom = 4    # zoom factor
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)  # render page to an image
        try:
            os.makedirs(rootfolder + "/temp_" +
                        document_name + "/")
        except:
            print("temp folder exists")
        PAGEPATHPNG = rootfolder + "/temp_" + \
            document_name + "/" + str(page.number) + ".png"
        PAGEPATHPDF = rootfolder + "/temp_" + \
            document_name + "/" + str(page.number) + ".pdf"
        pix.save(PAGEPATHPNG)

        # Generate QR code
        order_number = order_numbers[page.number]
        qrCode = qrcode.make(str(order_number)+"/")
        try:
            os.makedirs(rootfolder + "/tempQR_" +
                        document_name + "/")
        except:
            print("temp qr folder exists")
        QRCODEPATHPNG = rootfolder + "/tempQR_" + \
            document_name + "/" + str(order_number) + ".png"
        qrCode.save(str(QRCODEPATHPNG))

        with pillow.open(PAGEPATHPNG) as page, pillow.open(QRCODEPATHPNG) as QRCode:
            # No transparency mask specified,
            # simulating an raster overlay
            page.paste(QRCode, (800, 1440))
            page.convert('RGB')
            page.save(PAGEPATHPDF)

        with open(PAGEPATHPDF, "rb") as file:
            pdf = PyPDF2.PdfReader(file)
            page0 = pdf.pages[0]
            # float representing scale factor - this happens in-place
            page0.scale_by(0.25)
            writer = PyPDF2.PdfWriter()  # create a writer to save the updated results
            writer.add_page(page0)
            with open(PAGEPATHPDF, "wb") as output:
                writer.write(output)

        new_files += [PAGEPATHPDF]
    document.close()
    print(new_files)
    return new_files
