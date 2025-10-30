#!/usr/bin/env python3

import os
import argparse
from pathlib import Path
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import multiprocessing
import threading

try:
    from PIL import Image
    import pytesseract
except ImportError as e:
    print("Required dependencies not installed. Please run:")
    print("pip install pillow pytesseract")
    sys.exit(1)

def process_single_image(args):
    """Process a single image - optimized for performance"""
    image_path, output_folder, language = args

    try:
        image_file = os.path.basename(image_path)
        image_stem = Path(image_file).stem
        output_txt_path = os.path.join(output_folder, f"{image_stem}.txt")

        if os.path.exists(output_txt_path):
            return image_file, "skipped", 0, 0

        with Image.open(image_path) as img:
            if img.mode in ('P', 'RGBA', 'LA'):
                img = img.convert('RGB')

            ocr_config = '--oem 3 --psm 6'
            text = pytesseract.image_to_string(img, config=ocr_config, lang=language)
            text = text.strip()

        with open(output_txt_path, 'w', encoding='utf-8', errors='replace') as f:
            f.write(text)

        char_count = len(text)
        word_count = len(text.split()) if text else 0

        return image_file, "success", char_count, word_count

    except Exception as e:
        return image_file, f"error: {str(e)}", 0, 0

def fast_ocr_images(input_folder, output_folder, language='eng', max_workers=None):
    """True fast parallel OCR using threading"""

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

    actual_workers = max_workers if max_workers is not None else os.cpu_count()
    print(f"Found {total_files} images for TRUE FAST parallel OCR")
    print(f"Using {actual_workers} threads")  # Show actual thread count
    print(f"Language: {language}")
    print("-" * 50)

    start_time = time.time()
    success_count = 0
    completed_count = 0
    lock = threading.Lock()

    def process_image_thread(args):
        nonlocal success_count, completed_count
        image_path, output_folder, language = args

        try:
            image_file = os.path.basename(image_path)
            image_stem = Path(image_file).stem
            output_txt_path = os.path.join(output_folder, f"{image_stem}.txt")

            if os.path.exists(output_txt_path):
                with lock:
                    completed_count += 1
                    safe_file = image_file.encode('ascii', 'replace').decode('ascii')
                    print(f"[{completed_count}/{total_files}] {safe_file} - already processed")
                return

            with Image.open(image_path) as img:
                if img.mode in ('P', 'RGBA', 'LA'):
                    img = img.convert('RGB')

                text = pytesseract.image_to_string(img, lang=language)
                text = text.strip()

            with open(output_txt_path, 'w', encoding='utf-8', errors='replace') as f:
                f.write(text)

            char_count = len(text)

            with lock:
                success_count += 1
                completed_count += 1
                safe_file = image_file.encode('ascii', 'replace').decode('ascii')
                print(f"[{completed_count}/{total_files}] {safe_file} - {char_count} chars")

        except Exception as e:
            with lock:
                completed_count += 1
                safe_file = image_file.encode('ascii', 'replace').decode('ascii')
                print(f"[{completed_count}/{total_files}] {safe_file} - error: {str(e)}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_image_thread, (img_path, output_folder, language)) 
                  for img_path in image_paths]

        for future in as_completed(futures):
            future.result()

    end_time = time.time()
    processing_time = end_time - start_time

    print("-" * 50)
    print(f"Total processing time: {processing_time:.2f} seconds")
    print(f"Average: {processing_time/total_files:.2f} seconds per image")
    print(f"Speed: {total_files/processing_time:.2f} images/second")

    return success_count

def main():
    parser = argparse.ArgumentParser(
        description='Fast parallel OCR with language support',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('-i', '--input', required=True, 
                       help='Input folder with images')
    parser.add_argument('-o', '--output', required=True,
                       help='Output folder for TXT files')
    parser.add_argument('--workers', type=int, required=True,
                       help='Number of parallel workers (e.g., 4)')
    parser.add_argument('--lang', default='eng',
                       help='OCR language (vie, eng, vie+eng, etc. Default: eng)')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Input folder doesn't exist: {args.input}")
        sys.exit(1)

    print(f"Input: {args.input}")
    print(f"Output: {args.output}")

    success_count = fast_ocr_images(args.input, args.output, args.lang, args.workers)

    if success_count > 0:
        print(f"Successfully processed {success_count} files")
    else:
        print("No files processed")
        sys.exit(1)

if __name__ == "__main__":
    main()
