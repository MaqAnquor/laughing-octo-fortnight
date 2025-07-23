import os
import csv
import chardet
from pathlib import Path

def list_csv_files():
    cwd = Path.cwd()
    csv_files = list(cwd.glob("*.csv"))
    if not csv_files:
        print("No CSV files found in the current directory.")
        return None
    print("Available CSV files:")
    for idx, file in enumerate(csv_files, 1):
        print(f"{idx}. {file.name}")
    choice = int(input("Enter the number of the file to check: ")) - 1
    return csv_files[choice]

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']

def check_csv(file_path):
    errors = []
    encoding = detect_encoding(file_path)
    print(f"Detected encoding: {encoding}")

    try:
        with open(file_path, 'r', encoding=encoding, errors='replace') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader, None)
            if header is None:
                errors.append("Empty file or no header found.")
                return errors
            expected_len = len(header)

            for line_num, row in enumerate(reader, start=2):  # Line 1 is header
                if not any(row):
                    errors.append(f"Line {line_num}: Empty row")
                elif len(row) != expected_len:
                    errors.append(f"Line {line_num}: Expected {expected_len} columns, found {len(row)}")
    except Exception as e:
        errors.append(f"Could not read CSV: {e}")
    
    return errors

def main():
    selected_file = list_csv_files()
    if selected_file:
        print(f"\nChecking file: {selected_file.name}")
        errors = check_csv(selected_file)
        if errors:
            print("\n❌ Errors found:")
            for err in errors:
                print("-", err)
        else:
            print("\n✅ No errors found. File looks good.")

if __name__ == "__main__":
    main()
