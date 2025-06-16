# src/pdf_ingest.py

from pathlib import Path
from pdfminer.high_level import extract_text

# Paths
ROOT = Path(__file__).parent.parent
PDF_DIR = ROOT / "data" / "pdfs"
TXT_DIR = ROOT / "data" / "pdf_text"
TXT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDFs found in {PDF_DIR}.")
        return

    for pdf in pdf_files:
        text = extract_text(str(pdf))
        out_path = TXT_DIR / f"{pdf.stem}.txt"
        out_path.write_text(text, encoding="utf-8")
        print(f"  • {pdf.name} → {out_path.relative_to(ROOT)}")
    print("PDF ingestion complete.")


if __name__ == "__main__":
    main()
