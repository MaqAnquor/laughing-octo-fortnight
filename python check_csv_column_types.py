import csv
from pathlib import Path
from datetime import datetime

def select_csv_file():
    cwd = Path.cwd()
    csv_files = list(cwd.glob("*.csv"))
    if not csv_files:
        print("❌ No CSV files found in current directory.")
        return None

    print("📄 Available CSV files:")
    for idx, file in enumerate(csv_files, start=1):
        print(f"{idx}. {file.name}")

    try:
        choice = int(input("Enter the number of the file to check: "))
        if 1 <= choice <= len(csv_files):
            selected = csv_files[choice - 1]
            print(f"✅ Selected file: {selected.name}")
            return selected
        else:
            print("❌ Invalid selection. Please choose a number from the list.")
            return None
    except (ValueError, IndexError):
        print("❌ Invalid input. Please enter a number.")
        return None

def infer_type(value):
    value = value.strip()
    if value == "":
        return "empty"
    try:
        int(value)
        return "int"
    except:
        pass
    try:
        float(value)
        return "float"
    except:
        pass
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return "date"
    except:
        pass
    return "str"

def check_column_types_and_log_errors(csv_file_path):
    csv_file = Path(csv_file_path)
    if not csv_file.exists():
        print("❌ File does not exist.")
        return

    print("🔍 Reading and analyzing file...")
    with open(csv_file, 'r', encoding='utf-8-sig', errors='replace') as f:
        reader = list(csv.reader(f))
        if not reader:
            print("❌ Empty file.")
            return

        header = reader[0]
        rows = reader[1:]

        # Infer expected types per column
        expected_types = []
        for col_index in range(len(header)):
            col_vals = [row[col_index] for row in rows if len(row) > col_index and row[col_index].strip() != ""]
            col_type = infer_type(col_vals[0]) if col_vals else "str"
            expected_types.append(col_type)

        print("📌 Inferred column types:")
        for name, typ in zip(header, expected_types):
            print(f" - {name}: {typ}")

        # Check each value and collect mismatches
        log_entries = []
        for line_number, row in enumerate(rows, start=2):
            for col_index in range(len(header)):
                try:
                    value = row[col_index]
                except IndexError:
                    value = ""
                inferred_type = infer_type(value)
                expected = expected_types[col_index]
                if inferred_type != "empty" and inferred_type != expected:
                    log_entries.append(
                        f"Line {line_number}, Column '{header[col_index]}': "
                        f"Expected {expected}, found {inferred_type} — Value: '{value}'"
                    )

    # Write log to file
    log_file = csv_file.with_suffix('.log')
    with open(log_file, 'w', encoding='utf-8') as logf:
        logf.write(f"📋 Data Type Mismatch Report for {csv_file.name}\n")
        logf.write(f"{'-'*60}\n")
        if log_entries:
            for entry in log_entries:
                logf.write(entry + "\n")
            print(f"\n⚠️ {len(log_entries)} mismatches found. Logged to: {log_file.name}")
        else:
            logf.write("✅ No data type mismatches detected.\n")
            print("\n✅ No data type mismatches detected.")

def main():
    print("🔧 CSV Column Type Checker")
    file = select_csv_file()
    if file:
        check_column_types_and_log_errors(file)
    else:
        print("🚫 No file selected. Exiting.")

if __name__ == "__main__":
    main()
