import zipfile
import os
import argparse
import sys
from pathlib import Path

def extract_images_zip_method(docx_path, output_folder):
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(docx_path, 'r') as docx_zip:
            image_files = [f for f in docx_zip.namelist() if f.startswith('word/media/') and os.path.basename(f)]

            if not image_files:
                print("No images found in the document.")
                return 0, 0

            success_count = 0
            total_count = len(image_files)

            print(f"Found {total_count} images in document")

            for image_file in image_files:
                try:
                    filename = os.path.basename(image_file)
                    file_extension = Path(filename).suffix.lower()

                    if not file_extension:
                        with docx_zip.open(image_file) as f:
                            header = f.read(8)

                        if header.startswith(b'\x89PNG\r\n\x1a\n'):
                            file_extension = '.png'
                        elif header.startswith(b'\xff\xd8\xff'):
                            file_extension = '.jpg'
                        elif header.startswith(b'GIF8'):
                            file_extension = '.gif'
                        elif header.startswith(b'BM'):
                            file_extension = '.bmp'
                        else:
                            file_extension = '.png'

                    output_filename = f"{Path(filename).stem}{file_extension}"
                    output_path = os.path.join(output_folder, output_filename)

                    counter = 1
                    original_output_path = output_path
                    while os.path.exists(output_path):
                        name_part = Path(original_output_path).stem
                        ext_part = Path(original_output_path).suffix
                        output_path = os.path.join(output_folder, f"{name_part}_{counter:02d}{ext_part}")
                        counter += 1

                    with docx_zip.open(image_file) as image_data:
                        with open(output_path, 'wb') as f:
                            f.write(image_data.read())

                    file_size = os.path.getsize(output_path)
                    print(f"Extracted: {output_filename} ({file_size:,} bytes)")
                    success_count += 1

                except Exception as e:
                    print(f"Failed to extract {image_file}: {e}")

            return success_count

    except zipfile.BadZipFile:
        print("Error: The file is not a valid DOCX file or is corrupted")
        return 0, 0
    except FileNotFoundError:
        print(f"Error: File not found: {docx_path}")
        return 0, 0
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 0, 0

def main():
    parser = argparse.ArgumentParser(description='Extract images from DOCX files using zipfile method', formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-i', '--input', required=True, help='Input DOCX file path')
    parser.add_argument('-o', '--output', required=True, help='Output folder for extracted images')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file does not exist: {args.input}")
        sys.exit(1)

    if not args.input.lower().endswith('.docx'):
        print(f"Warning: Input file may not be a DOCX file: {args.input}")

    print(f"Processing: {args.input}")
    print(f"Output folder: {args.output}")
    print("-" * 50)

    success_count, total_count = extract_images_zip_method(args.input, args.output)

    print("-" * 50)
    if total_count > 0:
        if success_count == total_count:
            print(f"Successfully extracted all {success_count} images to: {args.output}")
        else:
            print(f"Extracted {success_count} out of {total_count} images to: {args.output}")
    else:
        print("No images were extracted")

if __name__ == "__main__":
    main()