import sys, os

"""
    The purpose of this script is to take an input file and
    report via an output file if there are any non-ascii characters.
"""

# Input File
input_file_name = "input_file.txt"
input_file = os.path.join(sys.path[0], input_file_name)

# Results/Output File
output_file_name = "Results.txt"
output_file = os.path.join(sys.path[0], output_file_name)

# Erase Output File
with open(output_file, "w") as f:
    pass


"""
    Read through the file and find non-ascii characters.
    If there is a non-ascii character, print it out to a results file.
"""
results = list()
row = 0

with open(input_file, "r") as f:
    for line in f:
        row += 1
        position = 0
        row_errors = list()
        for char in line:
            position += 1
            try:
                char.encode("ascii")
                pass  # This is an ascii character.
            except:
                row_errors.append(position)  # Store the position of the error.

        # Write out the combined results for the line
        if len(row_errors) > 0:
            with open(output_file, "a") as of:
                row_errors.sort()
                str_errors = ", ".join([str(x) for x in row_errors])
                of.write("Characters: {} ({})\n".format(str_errors, row))
                of.write("{}\n".format(line))
