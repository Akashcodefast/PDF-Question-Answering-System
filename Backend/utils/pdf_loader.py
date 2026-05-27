from PyPDF2 import PdfReader

def load_pdf_text(file_path):
    text = ""
    pdf_reader = pdfReader(file_path)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text
