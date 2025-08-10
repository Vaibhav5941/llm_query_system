import os
import django
import PyPDF2

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "llm_query_system.settings")
django.setup()

from core.models import Document

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def ingest_pdf(pdf_path):
    title = os.path.basename(pdf_path)
    file_path_relative = os.path.relpath(pdf_path, os.path.dirname(os.path.abspath(__file__)))

    if Document.objects.filter(title=title).exists():
        print(f"Document '{title}' already exists. Skipping ingestion.")
        return
    
    doc = Document(
        title=title,
        file_path=file_path_relative
    )
    doc.save()
    print(f"Saved Document '{title}' with file path '{file_path_relative}'.")

if __name__ == "__main__":
    pdf_folder = os.path.join(os.path.dirname(__file__), 'media')

    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith(".pdf"):
            full_path = os.path.join(pdf_folder, filename)
            print(f"Processing PDF: {full_path}")
            ingest_pdf(full_path)
