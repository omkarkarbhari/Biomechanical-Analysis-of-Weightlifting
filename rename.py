import os

# Path to the directory containing the images (change to your actual folder path)
folder_path = '/Users/shruti/Downloads/version1/frames'

# Iterate over all files in the directory
for filename in os.listdir(folder_path):
    # Check if the file has a .jpg extension
    if filename.lower().endswith('.jpg'):
        # Construct the new file name with .jpeg extension
        new_filename = filename[:-3] + 'jpeg'
        # Construct the full file paths
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)
        # Rename the file
        os.rename(old_file_path, new_file_path)

print("All .jpg files have been renamed to .jpeg successfully.")
