import os
import shutil

STATE_FILE = "move_state.txt"  # File to store the state

def move_file(source, destination, progress=None):
    with open(source, "rb") as fsrc:
        with open(destination, "ab") as fdst:
            if progress:
                fsrc.seek(progress)  # Set the file pointer to the progress position
            shutil.copyfileobj(fsrc, fdst)

def save_state(source, destination, progress):
    with open(STATE_FILE, "w") as f:
        f.write(f"{source}\n{destination}\n{progress}")

def load_state():
    if not os.path.exists(STATE_FILE):
        return None, None, None
    with open(STATE_FILE, "r") as f:
        lines = f.readlines()
        if len(lines) == 3:
            source = lines[0].strip()
            destination = lines[1].strip()
            progress = int(lines[2].strip())
            return source, destination, progress
    return None, None, None

def remove_state():
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)

# Load the previous state if available
source, destination, progress = load_state()

# If the previous state exists, move the file
if source and destination and progress:
    print("Resuming file move operation...")
    move_file(source, destination, progress)
    print("File move operation completed.")

    # Remove the state file
    remove_state()
else:
    # Perform the initial file move
    source = input("Enter the source file path: ")
    destination = input("Enter the destination file path: ")
    move_file(source, destination)
    print("File move operation completed.")

    # Save the state for future resumption
    save_state(source, destination, os.path.getsize(source))
