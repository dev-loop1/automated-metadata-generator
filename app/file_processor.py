import fitz  # PyMuPDF
import docx
import io
import pytesseract
from PIL import Image

def extract_text_from_pdf(file_stream):

    try:
        # --- Step 1: Attempt direct text extraction ---
        pdf_document = fitz.open(stream=file_stream, filetype="pdf")
        text = ""
        for page in pdf_document:
            text += page.get_text()
        
        # --- Step 2: If text is minimal, assume it's image-based and use OCR ---
        if len(text.strip()) < 100:
            print("Direct text extraction yielded minimal text. Attempting OCR...")
            text = ""  
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                
                pix = page.get_pixmap(dpi=300) 
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                # Tesseract to do OCR on the image
                text += pytesseract.image_to_string(img)
        
        pdf_document.close()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""


def extract_text_from_docx(file_stream):
    try:
        document = docx.Document(file_stream)
        full_text = []
        for para in document.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""

def extract_text_from_txt(file_stream):

    try:
        return file_stream.read().decode("utf-8")
    except Exception as e:
        print(f"Error extracting text from TXT: {e}")
        return ""
