import re
from pdfminer.high_level import extract_text

def extract_email(text):
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return match.group() if match else None

def extract_phone(text):
    match = re.search(r'\b\d{10}\b', text)
    return match.group() if match else None

def extract_name(text):
    lines = text.strip().split('\n')
    return lines[0] if lines else None

def parse_resume(file_path):
    text = extract_text(file_path)

    return {
        "Name": extract_name(text),
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "Summary": text[:500] + "..."  # Preview
    }
