import csv
from datetime import datetime
from pathlib import Path

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
        print("File does not exist.")
        return

    with open(csv_file, 'r', encoding='utf-8-sig', errors='replace') as f:
        reader = list(csv.reader(f))
        if not reader:
            print("Empty file.")
            return

        header = reader[0]
        rows = reader[1:]

        # Infer expected types from first non-empty row values
        expected_types = []
        for col_index in range(len(header)):
            col_vals = [row[col_index] for row in rows if row[col_index].strip() != ""]
            col_type = infer_type(col_vals[0]) if col_vals else "str"
            expected_types.append(col_type)

        log_entries = []
        for line_number, row in enumerate(rows, start=2):  # Starting from line 2 (after header)
            for col_index, value in enumerate(row):
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
        logf.write(f"Data Type Mismatch Report for {csv_file.name}\n")
        logf.write(f"{'-'*60}\n")
        if log_entries:
            for entry in log_entries:
                logf.write(entry + "\n")
            print(f"⚠️ Mismatches logged to: {log_file.name}")
        else:
            logf.write("✅ No data type mismatches detected.\n")
            print("✅ No data type mismatches detected.")
