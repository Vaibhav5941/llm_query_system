import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    """Extract full text from PDF using PyMuPDF"""
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

def extract_clauses(text):
    import re
    # Same regex pattern you had
    clause_pattern = r'(?i)(?=\n?(section|clause)?\s?\d{1,3}[\.:\)]\s)'
    raw_clauses = re.split(clause_pattern, text)

    combined_clauses = []
    for i in range(0, len(raw_clauses) - 1, 2):
        heading = (raw_clauses[i] or "").strip()
        part1 = (raw_clauses[i+1] or "").strip()
        part2 = (raw_clauses[i+2] or "").strip() if i+2 < len(raw_clauses) else ""
        clause = f"{heading} {part1} {part2}".strip()
        if len(clause) > 100:
            combined_clauses.append(clause)

    return combined_clauses


def parse_pdf_to_clauses(pdf_path):
    """Full pipeline: PDF → raw text → clauses"""
    text = extract_text_from_pdf(pdf_path)
    clauses = extract_clauses(text)
    return clauses
