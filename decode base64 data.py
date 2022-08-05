from pathlib import Path
import base64

# Input and Output Files
input_file_path = Path.cwd() / "input_file.txt"
output_file_path = Path.cwd() / "output.jpg"

# Open file. 
# Expects one base64 encoded string on the first line
with open(input_file_path, "r") as f:
    content = f.readline()

# base64 decode the data
b = base64.b64decode(content)

# Write the data into an output file
with open(output_file_path, "wb") as f:
    f.write(b)
