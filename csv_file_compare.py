import csv, os, sys

# File Names (with .csv extension)
file_1_name = "file_1.csv"
file_2_name = "file_2.csv"

results_file_name = "Compare Results.csv"
key = "worker_id"

# Get Paths to files
file_1_path = os.path.join(sys.path[0], "data_in", file_1_name)
file_2_path = os.path.join(sys.path[0], "data_in", file_2_name)
results_file_path = os.path.join(sys.path[0], "data_out", results_file_name)

d_errors = list()


# Read in file 1:
print("Reading file 1 to dictionary")
file_1 = list()
with open(file_1_path, mode="r", encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile, dialect="excel")
    for row in reader:
        file_1.append(dict(row))
file_1_columns = list(file_1[0].keys())


# Read in file 2:
print("Reading file 2 to dictionary")
file_2 = list()
with open(file_2_path, mode="r", encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        file_2.append(dict(row))
file_2_columns = list(file_2[0].keys())


# Get a distinct list of the columns to compare that match in both files
columns = list(set(file_2_columns) & set(file_1_columns))
columns.sort()
columns.remove(key)

# Compare File 1 to File 2
print("Comparing File 1 to File 2...")
for f1_row in file_1:
    for f2_row in file_2:
        if (
            f1_row[key] != f2_row[key]
        ):  # Cycle through data keys until employee is found
            continue
        for col in columns:
            if f1_row[col] == f2_row[col]:
                continue
            else:
                d = dict()
                d[key] = f1_row[key]
                d["column"] = col
                d["f1_value"] = f1_row[col]
                d["f2_value"] = f2_row[col]
                d_errors.append(d)
        break


# Find Workers in File 1, missing from File 2
for f1_row in file_1:
    match_test = 0
    for f2_row in file_2:
        if f1_row[key] == f2_row[key]:
            match_test = 1
            break
    if match_test != 1:
        d = dict()
        d[key] = f1_row[key]
        d["column"] = key
        d["f1_value"] = f1_row[key]
        d["f2_value"] = ""
        d_errors.append(d)

# Find Workers in File 2, missing from File 1
for f2_row in file_2:
    match_test = 0
    for f1_row in file_1:
        if f1_row[key] == f2_row[key]:
            match_test = 1
            break
    if match_test != 1:
        d = dict()
        d[key] = f2_row[key]
        d["column"] = key
        d["f1_value"] = ""
        d["f2_value"] = f2_row[key]
        d_errors.append(d)


# Write the results to a csv file
with open(results_file_path, "w") as csvfile:
    fieldnames = [key, "column", "f1_value", "f2_value"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(d_errors)
