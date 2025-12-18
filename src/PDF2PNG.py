import os
import sys
import argparse
from pathlib import Path
import fitz

def extract_images_from_pdf(pdf_path, output_folder, dpi=200):
    if not os.path.exists(pdf_path):
        print(f"PDF file not found: {pdf_path}")
        return 0

    Path(output_folder).mkdir(parents=True, exist_ok=True)

    print(f"Converting PDF with PyMuPDF at {dpi} DPI...")

    try:
        pdf = fitz.open(pdf_path)
        zoom = dpi / 72.0
        matrix = fitz.Matrix(zoom, zoom)

        for i, page in enumerate(pdf, 1):
            pix = page.get_pixmap(matrix=matrix)
            output_filename = f"page_{i:03d}.png"
            output_path = os.path.join(output_folder, output_filename)
            pix.save(output_path)
            print(f"Saved: {output_filename}")

        page_count = len(pdf)
        pdf.close()
        print(f"Successfully extracted {page_count} pages")
        return page_count

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return 0

def main():
    parser = argparse.ArgumentParser(description='Extract images from PDF to PNG files.', prog='PDF2PNG')
    parser.add_argument('-i', '--input', required=True, help='Path to the input PDF file')
    parser.add_argument( '-o', '--output', required=True, help='Path to the output folder for PNG images')
    parser.add_argument('--dpi', type=int, default=200, help='Resolution for output images in DPI (default: 200)')

    args = parser.parse_args()

    print(f"PDF2PNG - Processing: {args.input}")

    count = extract_images_from_pdf(args.input, args.output, args.dpi, args.use_pymupdf)

    if count > 0:
        print(f"Successfully converted {count} pages.")
        print(f"Output: {args.output}")
    else:
        print("Conversion failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()