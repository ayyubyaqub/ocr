import pytesseract
from PIL import Image
import re

pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe" #add your tesseract path 
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    bold_words = re.findall(r'\b[A-Z]{2,}\b', text)    
    return text, bold_words
