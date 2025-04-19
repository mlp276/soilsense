import os
import shutil
import csv

def process_folders(csv_file, base_path, dest_folder):
    # Create destination folder if it doesn't exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Read folder names from CSV
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        folder_names = [row[0] for row in reader]

    for folder_name in folder_names:
        folder_path = os.path.join(base_path, folder_name)

        if not os.path.isdir(folder_path):
            print(f"Folder not found: {folder_path}")
            continue

        # Look for a file named "mask" in the folder
        for file in os.listdir(folder_path):
            if file == "rgb.tif":
                src_file_path = os.path.join(folder_path, file)
                file_ext = os.path.splitext(file)[1]
                new_filename = f"rgb_{folder_name}{file_ext}"
                dest_file_path = os.path.join(dest_folder, new_filename)

                # Copy and rename the file
                shutil.copy(src_file_path, dest_file_path)
                print(f"Copied: {file} from {folder_name} -> {new_filename}")
                break  # Stop after finding the first "mask" in the folder
        else:
            print(f"No 'mask' file found in {folder_name}")

# === USAGE ===
csv_file = 'C:/Users/Dell/Box/My_Box_Notes/Rutgers/projects/soilsense/folder_names.csv'         # CSV with folder names (one per line)
base_path = 'C:/Users/Dell/Box/My_Box_Notes/Rutgers/projects/foldersfordata'            # Where all folders are located
dest_folder = 'C:/Users/Dell/Box/My_Box_Notes/Rutgers/projects/finishedfolders/rgb'        # Where renamed files go

process_folders(csv_file, base_path, dest_folder)
