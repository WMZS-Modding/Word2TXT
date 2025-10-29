#!/usr/bin/env python3

import os
import argparse
from pathlib import Path
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
import time

try:
    from PIL import Image
    import pytesseract
except ImportError as e:
    print("Required dependencies not installed. Please run:")
    print("pip install pillow pytesseract")
    sys.exit(1)

def process_single_image(args):
    """Process a single image - optimized for performance"""
    image_path, output_folder = args
    
    try:
        image_file = os.path.basename(image_path)
        image_stem = Path(image_file).stem
        output_txt_path = os.path.join(output_folder, f"{image_stem}.txt")

        if os.path.exists(output_txt_path):
            return image_file, "skipped", 0, 0

        with Image.open(image_path) as img:
            if img.mode in ('P', 'RGBA', 'LA'):
                img = img.convert('RGB')

            text = pytesseract.image_to_string(img, config='--oem 3 --psm 6')
            text = text.strip()

        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        char_count = len(text)
        word_count = len(text.split()) if text else 0
        
        return image_file, "success", char_count, word_count
        
    except Exception as e:
        return image_file, f"error: {str(e)}", 0, 0

def fast_ocr_images(input_folder, output_folder, max_workers=None):
    """Fast parallel OCR processing"""
    
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif'}
    image_paths = []
    
    for f in os.listdir(input_folder):
        if os.path.splitext(f)[1].lower() in image_extensions:
            image_paths.append(os.path.join(input_folder, f))
    
    if not image_paths:
        print("No image files found")
        return 0
    
    image_paths.sort()
    total_files = len(image_paths)
    
    print(f"Found {total_files} images for FAST parallel OCR")
    print(f"Using {max_workers or os.cpu_count()} CPU cores")
    print("-" * 50)
    
    start_time = time.time()
    success_count = 0

    process_args = [(img_path, output_folder) for img_path in image_paths]
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {
            executor.submit(process_single_image, args): args[0] 
            for args in process_args
        }

        for i, future in enumerate(as_completed(future_to_file), 1):
            image_file, status, char_count, word_count = future.result()
            
            if status == "success":
                print(f"[{i}/{total_files}] {image_file} - {char_count} chars")
                success_count += 1
            elif status == "skipped":
                print(f"[{i}/{total_files}] {image_file} - already processed")
                success_count += 1
            else:
                print(f"[{i}/{total_files}] {image_file} - {status}")
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    print("-" * 50)
    print(f"Total processing time: {processing_time:.2f} seconds")
    print(f"Average: {processing_time/total_files:.2f} seconds per image")
    
    return success_count

def main():
    parser = argparse.ArgumentParser(
        description='Fast parallel OCR for large image folders',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-i', '--input', required=True, 
                       help='Input folder with images')
    parser.add_argument('-o', '--output', required=True,
                       help='Output folder for TXT files')
    parser.add_argument('--workers', type=int, 
                       help='Number of parallel workers (default: CPU count)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Input folder doesn't exist: {args.input}")
        sys.exit(1)
    
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    
    success_count = fast_ocr_images(args.input, args.output, args.workers)
    
    if success_count > 0:
        print(f"Successfully processed {success_count} files")
    else:
        print("No files processed")
        sys.exit(1)

if __name__ == "__main__":
    main()