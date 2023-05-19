from PyPDF2 import PdfReader
import re


def extract_text_from_pdf(path):
    with open(path, "rb") as file:
        pdf = PdfReader(file)
        num_pages = len(pdf.pages)

        for page_number in range(num_pages):
            page = pdf.pages[page_number]
            text = page.extract_text()
            match = re.search(r'Ref1: (\d+)', text)
            if match:
                order_number = match.group(1)
                print(f"Order number on page {page_number+1}: {order_number}")
            else:
                print(f"No order number found on page {page_number+1}")


extract_text_from_pdf('C:/Users/info/Downloads/test.pdf')
