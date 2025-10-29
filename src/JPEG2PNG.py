#!/usr/bin/env python3

import os
import argparse
from pathlib import Path
import sys

try:
    from PIL import Image
except ImportError:
    print("PIL/Pillow not installed. Please run: pip install pillow")
    sys.exit(1)

def convert_jpeg_to_png(input_folder, output_folder, quality=95):
    """Convert all JPEG images to PNG format"""
    
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    jpeg_extensions = {'.jpg', '.jpeg', '.jpe', '.jfif'}
    jpeg_files = []
    
    for f in os.listdir(input_folder):
        file_path = os.path.join(input_folder, f)
        if os.path.isfile(file_path) and os.path.splitext(f)[1].lower() in jpeg_extensions:
            jpeg_files.append(f)
    
    if not jpeg_files:
        print("No JPEG files found in the input folder")
        return 0
    
    jpeg_files.sort()
    
    print(f"Found {len(jpeg_files)} JPEG files for conversion")
    print("-" * 50)
    
    success_count = 0
    for jpeg_file in jpeg_files:
        try:
            input_path = os.path.join(input_folder, jpeg_file)
            output_filename = Path(jpeg_file).stem + '.png'
            output_path = os.path.join(output_folder, output_filename)

            with Image.open(input_path) as img:
                if img.mode in ('P', 'RGBA', 'LA'):
                    img = img.convert('RGB')

                img.save(output_path, 'PNG', optimize=True)

            input_size = os.path.getsize(input_path)
            output_size = os.path.getsize(output_path)
            
            print(f"Converted: {jpeg_file} → {output_filename}")
            print(f"Size: {input_size:,} bytes → {output_size:,} bytes")
            
            success_count += 1
            
        except Exception as e:
            print(f"Failed to convert {jpeg_file}: {e}")
    
    return success_count

def convert_png_to_jpeg(input_folder, output_folder, quality=85):
    """Convert all PNG images to JPEG format (bonus function)"""
    
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    png_files = [f for f in os.listdir(input_folder) 
                if f.lower().endswith('.png') and os.path.isfile(os.path.join(input_folder, f))]
    
    if not png_files:
        print("No PNG files found in the input folder")
        return 0
    
    png_files.sort()
    
    print(f"Found {len(png_files)} PNG files for conversion to JPEG")
    print("-" * 50)
    
    success_count = 0
    for png_file in png_files:
        try:
            input_path = os.path.join(input_folder, png_file)
            output_filename = Path(png_file).stem + '.jpg'
            output_path = os.path.join(output_folder, output_filename)
            
            with Image.open(input_path) as img:
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')

                img.save(output_path, 'JPEG', quality=quality, optimize=True)
            
            input_size = os.path.getsize(input_path)
            output_size = os.path.getsize(output_path)
            
            print(f"Converted: {png_file} → {output_filename}")
            print(f"Size: {input_size:,} bytes → {output_size:,} bytes")
            print(f"Compression: {((input_size - output_size) / input_size * 100):.1f}% reduction")
            
            success_count += 1
            
        except Exception as e:
            print(f"Failed to convert {png_file}: {e}")
    
    return success_count

def main():
    parser = argparse.ArgumentParser(
        description='Convert between JPEG and PNG formats',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-i', '--input', required=True, 
                       help='Input folder containing images')
    parser.add_argument('-o', '--output', required=True,
                       help='Output folder for converted images')
    parser.add_argument('--to', choices=['png', 'jpeg'], default='png',
                       help='Target format (default: png)')
    parser.add_argument('--quality', type=int, default=85,
                       help='JPEG quality (1-100, default: 85)')
    
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input folder does not exist: {args.input}")
        sys.exit(1)
    
    print(f"Input folder: {args.input}")
    print(f"Output folder: {args.output}")
    print(f"Target format: {args.to.upper()}")
    print("-" * 50)
    
    if args.to == 'png':
        success_count = convert_jpeg_to_png(args.input, args.output)
    else:
        success_count = convert_png_to_jpeg(args.input, args.output, args.quality)
    
    print("-" * 50)
    if success_count > 0:
        print(f"Successfully converted {success_count} images")
        print(f"Output folder: {args.output}")
    else:
        print("No images were converted successfully")
        sys.exit(1)

if __name__ == "__main__":
    main()