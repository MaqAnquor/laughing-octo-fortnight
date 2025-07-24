import csv
from pathlib import Path
from datetime import datetime

def select_csv_file():
    cwd = Path.cwd()
    csv_files = list(cwd.glob("*.csv"))
    if not csv_files:
        print("❌ No CSV files found in current directory.")
        return None
    print("\n📄 Available CSV files:")
    for idx, file in enumerate(csv_files, 1):
        print(f"{idx}. {file.name}")
    while True:
        try:
            choice = int(input("Enter the number of the CSV file to select: "))
            if 1 <= choice <= len(csv_files):
                print(f"✅ Selected file: {csv_files[choice-1].name}")
                return csv_files[choice-1]
            else:
                print("❌ Please enter a valid number from the list.")
        except ValueError:
            print("❌ Please enter a number.")

def get_headers(csv_file):
    with open(csv_file, 'r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.reader(f)
        header = next(reader, None)
    return header

def log_headers(headers, csv_file):
    log_file = Path(csv_file).with_suffix('.headers.txt')
    with open(log_file, 'w', encoding='utf-8') as logf:
        for col in headers:
            logf.write(col + "\n")
    print(f"📋 Headers logged to: {log_file.name}")

def select_header(headers):
    print("\n🔢 Headers in selected file:")
    for idx, col in enumerate(headers, 1):
        print(f"{idx}. {col}")
    while True:
        try:
            choice = int(input("Select the header number to check for dd-mm-yyyy dates: "))
            if 1 <= choice <= len(headers):
                print(f"✅ Selected header: {headers[choice-1]}")
                return headers[choice-1]
            else:
                print("❌ Please enter a valid number from the list.")
        except ValueError:
            print("❌ Please enter a number.")

def is_valid_dd_mm_yyyy(value):
    try:
        datetime.strptime(value.strip(), '%d-%m-%Y')
        return True
    except Exception:
        return False

def check_column_for_dd_mm_yyyy_dates(csv_file, header):
    log_entries = []
    with open(csv_file, 'r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.DictReader(f)
        line_num = 2  # Header is line 1
        for row in reader:
            value = row.get(header, "").strip()
            if value == "":
                log_entries.append(f"Line {line_num}: MISSING value")
            elif not is_valid_dd_mm_yyyy(value):
                log_entries.append(f"Line {line_num}: '{value}' (INVALID FORMAT)")
            line_num += 1
    return log_entries

def main():
    print("🔍 CSV File & Column dd-mm-yyyy Date Checker")
    file = select_csv_file()
    if not file:
        print("🚫 No file selected. Exiting.")
        return

    headers = get_headers(file)
    if not headers:
        print("❌ Could not read headers from file.")
        return

    print("\nHeaders found in file:")
    for col in headers:
        print(f"- {col}")
    log_headers(headers, file)

    header = select_header(headers)
    print(f"\n🔎 Checking if all values in column '{header}' are dates (dd-mm-yyyy)...")

    log_entries = check_column_for_dd_mm_yyyy_dates(file, header)

    log_file = Path(f"{header}.log")
    with open(log_file, 'w', encoding='utf-8') as lf:
        if log_entries:
            lf.write(f"Issues in column '{header}':\n")
            lf.write('\n'.join(log_entries))
            print(f"\n❌ {len(log_entries)} issues found. Details logged in: {log_file.name}")
        else:
            lf.write(f"✅ All values in column '{header}' are valid dd-mm-yyyy dates.\n")
            print(f"\n✅ All values in column '{header}' are valid dd-mm-yyyy dates.")

if __name__ == "__main__":
    main()
