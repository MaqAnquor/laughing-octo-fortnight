import os
from pathlib import Path
import chardet

def list_csv_files():
    cwd = Path.cwd()
    csv_files = list(cwd.glob("*.csv"))
    if not csv_files:
        print("No CSV files found in the current directory.")
        return None
    print("Available CSV files:")
    for idx, file in enumerate(csv_files, 1):
        print(f"{idx}. {file.name}")
    choice = int(input("Enter the number of the file to convert: ")) - 1
    return csv_files[choice]

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']

def convert_to_ascii(source_file):
    encoding = detect_encoding(source_file)
    print(f"Detected encoding: {encoding}")

    try:
        with open(source_file, 'r', encoding=encoding, errors='replace') as src:
            content = src.read()

        # Convert to ASCII (replace non-ASCII with '?')
        ascii_content = content.encode('ascii', errors='replace').decode('ascii')

        target_file = source_file.with_name(source_file.stem + '_ascii.csv')
        with open(target_file, 'w', encoding='ascii', errors='replace') as dest:
            dest.write(ascii_content)

        print(f"✅ File converted and saved as: {target_file.name}")
    except Exception as e:
        print(f"❌ Error during conversion: {e}")

def main():
    selected_file = list_csv_files()
    if selected_file:
        convert_to_ascii(selected_file)

if __name__ == "__main__":
    main()
