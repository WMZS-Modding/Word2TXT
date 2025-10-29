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

def ocr_images_to_individual_files(input_folder, output_folder, language='eng'):
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
    print(f"Language: {language}")
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

                text = pytesseract.image_to_string(img, lang=language)
                text = text.strip()

            with open(output_txt_path, 'w', encoding='utf-8', errors='replace') as f:
                f.write(text)
            
            char_count = len(text)
            word_count = len(text.split()) if text else 0

            safe_image_file = image_file.encode('ascii', 'replace').decode('ascii')
            safe_txt_file = output_txt_file.encode('ascii', 'replace').decode('ascii')
            print(f"Processed {i}/{len(image_files)}: {safe_image_file} -> {safe_txt_file}")
            print(f"   {char_count} characters, {word_count} words")
            
            success_count += 1
            
        except UnicodeEncodeError as e:
            safe_image_file = image_file.encode('ascii', 'replace').decode('ascii')
            print(f"Processed {i}/{len(image_files)}: {safe_image_file} -> {output_txt_file}")
            print(f"   Note: Contains special characters that can't be displayed in console")
            success_count += 1
        except Exception as e:
            error_msg = f"Failed to process {image_file}: {e}"
            print(error_msg)
    
    return success_count

def main():
    parser = argparse.ArgumentParser(
        description='Single-thread OCR with language support',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-i', '--input', required=True, 
                       help='Input folder containing images')
    parser.add_argument('-o', '--output', required=True,
                       help='Output folder for TXT files')
    parser.add_argument('--lang', default='eng',
                       help='OCR language (vie, eng, vie+eng, etc. Default: eng)')
    
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input folder does not exist: {args.input}")
        sys.exit(1)
    
    print(f"Input folder: {args.input}")
    print(f"Output folder: {args.output}")
    print(f"OCR Language: {args.lang}")
    print("-" * 50)
    
    success_count = ocr_images_to_individual_files(args.input, args.output, args.lang)
    
    print("-" * 50)
    if success_count > 0:
        print(f"Successfully processed {success_count} images")
        print(f"TXT files saved to: {args.output}")

        txt_files = [f for f in os.listdir(args.output) if f.endswith('.txt')]
        if txt_files:
            print(f"Created {len(txt_files)} text files")
            if len(txt_files) <= 5:
                for txt_file in txt_files[:5]:
                    safe_txt_file = txt_file.encode('ascii', 'replace').decode('ascii')
                    print(f"   {safe_txt_file}")
            else:
                for txt_file in txt_files[:3]:
                    safe_txt_file = txt_file.encode('ascii', 'replace').decode('ascii')
                    print(f"   {safe_txt_file}")
                print(f"   ... and {len(txt_files) - 3} more")
    else:
        print("No images were processed successfully")
        sys.exit(1)

if __name__ == "__main__":
    main()