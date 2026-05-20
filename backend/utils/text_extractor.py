"""
Text Extraction Module
Extracts text from PDF, DOCX, and image files
"""

import PyPDF2
from docx import Document
import pytesseract
from PIL import Image
import os
import sys
import warnings
import io

warnings.filterwarnings('ignore')

# Configure pytesseract to find Tesseract
# Common paths on Windows
possible_paths = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    r"C:\Users\TUNNA\AppData\Local\Tesseract-OCR\tesseract.exe",
]

# Try to set the pytesseract path
for path in possible_paths:
    if os.path.exists(path):
        pytesseract.pytesseract.pytesseract_cmd = path
        print(f"[TEXT_EXTRACTOR] Tesseract found at: {path}")
        break
else:
    print(f"[TEXT_EXTRACTOR] WARNING: Tesseract not found in standard locations")
    print(f"[TEXT_EXTRACTOR] Install from: https://github.com/UB-Mannheim/tesseract/wiki")
    print(f"[TEXT_EXTRACTOR] Expected in one of: {possible_paths}")


def extract_from_pdf(file_path):
    """Extract text from PDF file - uses PyMuPDF for text extraction and OCR for scanned PDFs"""
    try:
        print(f"[TEXT_EXTRACTOR] Attempting text extraction from PDF: {file_path}")
        text = ""
        
        # First try: PyPDF2 for text extraction
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"[TEXT_EXTRACTOR] PyPDF2 extraction attempt failed: {str(e)}")
        
        # If we got text, return it
        if text and text.strip():
            print(f"[TEXT_EXTRACTOR] Successfully extracted text from PDF ({len(text)} chars)")
            return text
        
        # Second try: PyMuPDF for better text extraction
        try:
            import fitz  # PyMuPDF
            print(f"[TEXT_EXTRACTOR] Attempting PyMuPDF text extraction...")
            
            doc = fitz.open(file_path)
            fitz_text = ""
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                fitz_text += page.get_text()
            
            doc.close()
            
            if fitz_text and fitz_text.strip():
                print(f"[TEXT_EXTRACTOR] PyMuPDF extraction successful ({len(fitz_text)} chars)")
                return fitz_text
        except Exception as e:
            print(f"[TEXT_EXTRACTOR] PyMuPDF extraction failed: {str(e)}")
        
        # Third try: OCR using PyMuPDF to render pages
        if text.strip() or True:  # Try OCR if text extraction found nothing or less
            print(f"[TEXT_EXTRACTOR] No/insufficient text found, attempting OCR with PyMuPDF rendering...")
            try:
                import fitz
                
                doc = fitz.open(file_path)
                ocr_text = ""
                
                for page_num in range(len(doc)):
                    print(f"[TEXT_EXTRACTOR] Processing page {page_num + 1}/{len(doc)} with OCR...")
                    page = doc[page_num]
                    
                    # Render page to image at higher DPI (300)
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    
                    # Extract text using OCR
                    page_text = pytesseract.image_to_string(img)
                    if page_text.strip():
                        ocr_text += page_text + "\n"
                
                doc.close()
                
                if ocr_text.strip():
                    combined_text = text + "\n" + ocr_text if text.strip() else ocr_text
                    print(f"[TEXT_EXTRACTOR] OCR successful ({len(combined_text)} chars)")
                    return combined_text
                else:
                    print(f"[TEXT_EXTRACTOR] OCR found no text")
                    return text if text.strip() else "No text found in PDF (scanned document with no readable content)"
            
            except ImportError:
                print(f"[TEXT_EXTRACTOR] PyMuPDF not installed")
                return text if text.strip() else "No text found in PDF. Install PyMuPDF: pip install PyMuPDF"
            except Exception as ocr_error:
                error_msg = str(ocr_error)
                if "tesseract" in error_msg.lower() or "not installed" in error_msg.lower():
                    print(f"[TEXT_EXTRACTOR] Tesseract not found for OCR: {error_msg}")
                    return text if text.strip() else f"[SYSTEM SETUP REQUIRED] Tesseract OCR is not installed. Basic text extraction found no text. Please install Tesseract OCR for scanned PDF support.\n- Windows: https://github.com/UB-Mannheim/tesseract/wiki\n- macOS: brew install tesseract\n- Linux: sudo apt-get install tesseract-ocr"
                else:
                    print(f"[TEXT_EXTRACTOR] OCR conversion failed: {error_msg}")
                    return text if text.strip() else f"PDF text extraction failed: {error_msg}"
    
    except Exception as e:
        print(f"[TEXT_EXTRACTOR] PDF extraction error: {str(e)}")
        return f"Error extracting PDF: {str(e)}"


def extract_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        print(f"[TEXT_EXTRACTOR] Extracting text from DOCX: {file_path}")
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        print(f"[TEXT_EXTRACTOR] DOCX extraction successful ({len(text)} chars)")
        return text if text else "No text found in DOCX"
    except Exception as e:
        print(f"[TEXT_EXTRACTOR] DOCX extraction error: {str(e)}")
        return f"Error extracting DOCX: {str(e)}"


def extract_from_image(file_path):
    """Extract text from image file using OCR"""
    try:
        print(f"[TEXT_EXTRACTOR] Extracting text from image with OCR: {file_path}")
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        print(f"[TEXT_EXTRACTOR] Image OCR successful ({len(text)} chars)")
        return text if text else "No text found in image"
    except Exception as e:
        error_msg = str(e)
        # Check if Tesseract is not installed
        if "tesseract" in error_msg.lower() or "not installed" in error_msg.lower():
            print(f"[TEXT_EXTRACTOR] Tesseract not found: {error_msg}")
            return f"[SYSTEM SETUP REQUIRED] Tesseract OCR is not installed. Please install it:\n- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki\n- macOS: brew install tesseract\n- Linux: sudo apt-get install tesseract-ocr"
        else:
            print(f"[TEXT_EXTRACTOR] Image extraction error: {error_msg}")
            return f"Error extracting image: {error_msg}"


def extract_text(file_path):
    """
    Extract text from any supported file format
    
    Args:
        file_path: Path to the file
        
    Returns:
        Extracted text string
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return extract_from_pdf(file_path)
    elif file_extension == '.docx':
        return extract_from_docx(file_path)
    elif file_extension in ['.jpg', '.jpeg', '.png']:
        return extract_from_image(file_path)
    else:
        return f"Unsupported file format: {file_extension}"
