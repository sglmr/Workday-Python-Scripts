import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


# File Names (with .csv extension)
FILES = [
    BASE_DIR / "FILE_1.csv",
    BASE_DIR / "FILE_2.csv",
]

KEY = "ID_FIELD"

# Assert only comparing 2 files
assert len(FILES) == 2

OUTFILE = BASE_DIR / "COMPARE RESULTS.csv"

ERRORS = list()


class CSVFile:
    def __init__(self, file_path: Path, key: str):
        self.key = key

        assert file_path.suffix == ".csv"
        self.file_path = file_path

        # Read file into data_rows
        self.data_rows = dict()
        with open(self.file_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, dialect="excel")
            for count, row in enumerate(reader):
                row_key = row[self.key]
                self.data_rows[row_key] = row

                if count == 0:
                    # Use the first data row to get the column names
                    self.col_names = [f"{x}" for x in row.keys()]

                    assert self.key in self.col_names  # assert the key is in the file
                    assert len(self.col_names) == len(
                        set(self.col_names)
                    )  # Assert no duplicate column names

    def __str__(self):
        return f"{self.file_path.stem}"


# Create the CSVFile objects for each file
csv1 = CSVFile(file_path=FILES[0], key=KEY)
csv2 = CSVFile(file_path=FILES[1], key=KEY)


# Check for records in file 1, but not file 2
for k in csv1.data_rows.keys():
    found_record = csv2.data_rows.get(k, None)
    if found_record:
        for field in csv1.col_names:
            csv1_data = csv1.data_rows[k][field]
            csv2_data = csv2.data_rows[k].get(field, None)

            if csv1_data == csv2_data:
                continue
            elif csv1_data != csv2_data:
                if csv2_data:
                    note = "data mismatch"
                elif not csv2_data:
                    note = "missing field"

                ERRORS.append(
                    {
                        "key": k,
                        "col": field,
                        "f1": f"{csv1_data or ''}",
                        "f2": f"{csv2_data or ''}",
                        "notes": note,
                    }
                )
    else:
        ERRORS.append(
            {
                "key": k,
                "col": "",
                "f1": "",
                "f2": "",
                "notes": f"Record missing from {csv2}",
            }
        )

# Check for records in file 1, but not file 2
for k in csv2.data_rows.keys():
    found_record = csv1.data_rows.get(k, None)
    if found_record:
        for field in csv2.col_names:
            csv1_data = csv1.data_rows[k].get(field, None)
            csv2_data = csv2.data_rows[k][field]

            if csv1_data is None:
                ERRORS.append(
                    {
                        "key": k,
                        "col": field,
                        "f1": f"{csv1_data or ''}",
                        "f2": f"{csv2_data or ''}",
                        "notes": "missing field",
                    }
                )
            else:
                continue

    else:
        ERRORS.append(
            {
                "key": k,
                "col": "",
                "f1": "",
                "f2": "",
                "notes": f"Record missing from {csv1}",
            }
        )

# Write the results to a csv file
with open(OUTFILE, "w") as csvfile:

    writer = csv.writer(csvfile)
    writer.writerow([f"{KEY}", "Field", f"{csv1}", f"{csv2}", "Notes"])

    for err in ERRORS:
        writer.writerow([err["key"], err["col"], err["f1"], err["f2"], err["notes"]])
