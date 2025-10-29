#!/usr/bin/env python3

import os
import argparse
from pathlib import Path
import sys

try:
    from PIL import Image
    import pytesseract
except ImportError as e:
    print("Required dependencies not installed. Please run:")
    print("pip install pillow pytesseract")
    print("Also install Tesseract OCR:")
    print("Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
    print("Mac: brew install tesseract")
    print("Linux: sudo apt-get install tesseract-ocr")
    sys.exit(1)

def ocr_images_to_individual_files(input_folder, output_folder):
    """Perform OCR on all images and save individual text files"""

    Path(output_folder).mkdir(parents=True, exist_ok=True)

    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif', '.webp'}
    image_files = []
    
    for f in os.listdir(input_folder):
        file_path = os.path.join(input_folder, f)
        if os.path.isfile(file_path) and os.path.splitext(f)[1].lower() in image_extensions:
            image_files.append(f)
    
    if not image_files:
        print("No image files found in the input folder")
        return 0
    
    image_files.sort()
    
    print(f"Found {len(image_files)} images for OCR processing")
    print("-" * 50)
    
    success_count = 0
    for i, image_file in enumerate(image_files, 1):
        try:
            image_path = os.path.join(input_folder, image_file)

            image_stem = Path(image_file).stem
            output_txt_file = f"{image_stem}.txt"
            output_txt_path = os.path.join(output_folder, output_txt_file)

            with Image.open(image_path) as img:
                if img.mode in ('P', 'RGBA', 'LA'):
                    img = img.convert('RGB')

                text = pytesseract.image_to_string(img)

                text = text.strip()

            with open(output_txt_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            char_count = len(text)
            word_count = len(text.split()) if text else 0
            
            print(f"Processed {i}/{len(image_files)}: {image_file} → {output_txt_file}")
            print(f"{char_count} characters, {word_count} words")
            
            success_count += 1
            
        except Exception as e:
            error_msg = f"Failed to process {image_file}: {e}"
            print(error_msg)
    
    return success_count

def main():
    parser = argparse.ArgumentParser(
        description='Perform OCR on images and save individual text files',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-i', '--input', required=True, 
                       help='Input folder containing images from PDF conversion')
    parser.add_argument('-o', '--output', required=True,
                       help='Output folder for individual TXT files')
    
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input folder does not exist: {args.input}")
        sys.exit(1)
    
    print(f"Input folder: {args.input}")
    print(f"Output folder: {args.output}")
    print("-" * 50)
    
    success_count = ocr_images_to_individual_files(args.input, args.output)
    
    print("-" * 50)
    if success_count > 0:
        print(f"Successfully processed {success_count} images")
        print(f"TXT files saved to: {args.output}")

        txt_files = [f for f in os.listdir(args.output) if f.endswith('.txt')]
        if txt_files:
            print(f"Created {len(txt_files)} text files")
            if len(txt_files) <= 5:
                for txt_file in txt_files[:5]:
                    print(f"{txt_file}")
            else:
                for txt_file in txt_files[:3]:
                    print(f"{txt_file}")
                print(f"... and {len(txt_files) - 3} more")
    else:
        print("No images were processed successfully")
        sys.exit(1)

if __name__ == "__main__":
    main()