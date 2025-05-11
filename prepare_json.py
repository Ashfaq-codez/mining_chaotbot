import re
import json
from PyPDF2 import PdfReader

pdf_path = "MINES AND MINERALS (DEVELOPMENT AND REGULATION) ACT, 1957.pdf"
text_path = "MINES AND MINERALS (DEVELOPMENT AND REGULATION) ACT, 1957.txt"
json_path = "mining_chunks.json"

def extract_pdf():
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            page_text = re.sub(r'[^\x00-\x7F]+', '', page_text)
            text += page_text + "\n"

    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("✅ Extracted PDF text to .txt")

def chunk_text():
    with open(text_path, "r", encoding="utf-8") as f:
        full_text = f.read()

    pattern = r"(?=\n?\d+\.\s)"  # Example: Matches "\n1. ", "\n2. ", etc.
    sections = re.split(pattern, full_text)

    chunks = []
    for section in sections:
        lines = section.strip().splitlines()
        if not lines:
            continue
        title = lines[0].strip()
        content = "\n".join(lines[1:]).strip()
        if content:
            chunks.append({
                "section": title,
                "content": content
            })

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4)

    print(f"✅ Created {len(chunks)} structured chunks in mining_chunks.json")

if __name__ == "__main__":
    extract_pdf()
    chunk_text()
