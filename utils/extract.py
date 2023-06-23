# from PyPDF2 import PdfReader
import pytesseract
from PIL import Image

# from pdf2image import convert_from_path
import cv2
import glob
import os
import numpy as np


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"
# path = r"C:\path-files\poppler-23.01.0\Library\bin"


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 50, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# def process_scanned_documents():
#     scanned_files = glob.glob("scanned_docs\**.pdf")
#     for pdf in scanned_files:
#         print(f"Converting {pdf} to image...")
#         images = convert_from_path(pdf, poppler_path=path)
#         for i in range(len(images)):
#             #   Save pages as images in the pdf
#             images[i].save(f"pdf_2_image/{os.path.basename(pdf)}_{i}.jpg", "JPEG")


def extract_text(bytes_data, file_name):
    # extracted_images = glob.glob("pdf_2_image\**.jpg")
    all_text = ""
    # for img in extracted_images:
    # img = cv2.imread(img)
    img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    gray = get_grayscale(img)
    # blurred = remove_noise(gray)
    # thresh = thresholding(gray)
    all_text += pytesseract.image_to_string(gray)

    with open(f"{file_name}.txt", "w") as f:
        f.write(all_text)
