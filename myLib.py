import os

Script_Version = "1.0"

# Reads a bin file and returns the read bites as a bytearray.
def read_bytes_from_file(file, start, end):
    with open(file, 'rb') as f:
        f.seek(start)
        return bytearray(f.read(end - start))

# Reads bytes from a variable and writes them to a file on disk.
def write_bytes_to_file(data, file):
    with open(file, 'wb') as f:
        f.write(data)

# Asks the user if they want to do whatever they were about to do.
def reuse(Prompt):
    print(Prompt)
    while True:
        resp = input("(Y/N): ").upper()
        if resp == "N":
            return False
        elif resp == "Y":
            return True
        
# Sanity checking! Makes sure the file name provided matches a file in the right place of the right size. So I can pretend I tried...
def get_valid_file(Prompt):
    while True:
        file_name = input(Prompt)
        if os.path.exists(file_name) and os.path.getsize(file_name) == 131072:
            print(f"Confirmed. '{file_name}' has been found and will be used.")
            return file_name
        else:
            print(f"Invalid file: '{file_name}'. Please make sure '{file_name}' exists in '{os.getcwd()}' and is a 128KB bin file.")

# (In)Sanity checking! Make sure the file name provided doesn't match a file in the right place. If it does warn them before they can overwrite it.
def get_invalid_file(file_name):
    if not os.path.exists(file_name) or reuse(f"File with the name '{file_name}' already exists. Do you want to overwrite it?"):
        return True
    else:
        return False