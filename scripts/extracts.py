import os
from PyPDF2 import PdfReader

INPUT_PATH = "data/raw/rbi_annual_report_2023_24.pdf"
OUTPUT_PATH = "data/raw/all_text.txt"

def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    full_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text.append(text)
    return "\n\n".join(full_text)

def main():
    text = extract_text_from_pdf(INPUT_PATH)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[+] Extracted {len(text)} characters to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
