import sys
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

def extract_text_from_pdf(pdf_path):
    # Load the OCR model
    model = ocr_predictor(pretrained=True)

    # Load the PDF
    pdf = DocumentFile.from_pdf(pdf_path)

    # Perform OCR
    result = model(pdf)

    # Extract and print the text line by line
    for page in result.export()["pages"]:
        for block in page["blocks"]:
            for line in block["lines"]:
                print(" ".join([word["value"] for word in line["words"]]))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ocr_extractor.py <document_name.pdf>")
        sys.exit(1)

    pdf_filename = sys.argv[1]
    extract_text_from_pdf(pdf_filename)
