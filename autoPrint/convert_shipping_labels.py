from PIL import Image
from pypdf import PdfReader, PdfFileWriter
import PyPDF2

import fitz
import qrcode
import ntpath


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def genNew(path):
    id = path_leaf(path).split(".")[0]
    doc = fitz.open(path)
    for page in doc:
        zoom = 4    # zoom factor
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)  # render page to an image
        pix.save("temp.png")

    # import ImageWriter to generate an image file

    # Make sure to pass the number as string
    img = qrcode.make(str(id)+"/")
    type(img)  # qrcode.image.pil.PilImage
    img.save(str(id)+".png")

    img1 = Image.open(r"temp.png")
    width, height = img1.size
    img2 = Image.open(str(id)+".png")

    # No transparency mask specified,
    # simulating an raster overlay
    img1.paste(img2, (800, 1440))

    # img1.show()
    img1.convert('RGB')
    img1.save(path)

    pdf = path
    pdf = PyPDF2.PdfReader(pdf)
    page0 = pdf.pages[0]
    # float representing scale factor - this happens in-place
    page0.scale_by(0.25)
    writer = PyPDF2.PdfWriter()  # create a writer to save the updated results
    writer.add_page(page0)
    with open(path, "wb+") as f:
        writer.write(f)
