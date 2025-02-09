import os
from typing import Optional
import magic
import PyPDF2
from docx import Document

def extract_text_from_document(file_content: bytes, filename: str) -> Optional[str]:
    """Extract text from various document formats."""
    mime_type = magic.from_buffer(file_content, mime=True)
    
    if mime_type == 'text/plain':
        return file_content.decode('utf-8')
        
    elif mime_type == 'application/pdf':
        # Read PDF
        from io import BytesIO
        pdf_file = BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
        
    elif mime_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        # Read Word document
        from io import BytesIO
        doc = Document(BytesIO(file_content))
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
    else:
        raise ValueError(f"Unsupported file type: {mime_type}") 