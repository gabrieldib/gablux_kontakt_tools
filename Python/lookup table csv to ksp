import csv

# paths for the CSV file to be read and KSP output file
CSV_FILE_PATH = ""
KSP_FILE_PATH = ""

LOOKUP_TABLES_COUNT = 3 # as an example, say our CSV file has 3 curves

with open(CSV_FILE_PATH, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)

    # range starts at 1 considering the first column is the x value that generates the curves
    # check the 'cubeish_double_xfade.csv' file
    lookup_tables = [f"declare __CURVE_{n} [128] := (" for n in range(1,LOOKUP_TABLES_COUNT+1) ]

    for row in csv_reader:
        for table_index in range(0, len(lookup_tables)):
            lookup_tables[table_index] += row[table_index+1] + ","

    for table_index in range(0, len(lookup_tables)):
            lookup_tables[table_index] = lookup_tables[table_index][:-1] + ")"

    ksp_code = ""
    for table in lookup_tables:
        ksp_code += table + "\n"


with open(KSP_FILE_PATH, "w") as output_file:
    output_file.write(ksp_code)
