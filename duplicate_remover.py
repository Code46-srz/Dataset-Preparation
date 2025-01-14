import os
import hashlib

def remove_duplicate_images(folder_path, delete_duplicates=False):
    hash_map = {}
    duplicates = []
    
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return []
    
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            try:
                # Calculate the hash of the image file
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()

                # Print the file path and its hash
                print(f"File: {file_path}, Hash: {file_hash}")
                if file_hash in hash_map:
                    # Found a duplicate
                    print(f"Duplicate found: {file_path} (original: {hash_map[file_hash]})")
                    duplicates.append(file_path)
                    if delete_duplicates:
                        print(f"Deleting: {file_path}")
                        os.remove(file_path)  # Remove the duplicate
                else:
                    hash_map[file_hash] = file_path
            except Exception as e:
                print(f"Error processing file '{file_path}': {e}")
    
    print(f"Removed {len(duplicates)} duplicates")
    return duplicates

# Example usage
if __name__ == "__main__":
    folder = "/home/virtual46/tool_images"  # Ensure this path is correct
    delete_duplicates = True  # Set to True to enable deletion of duplicates

    duplicates = remove_duplicate_images(folder, delete_duplicates=delete_duplicates)
    print("\nDetected duplicates:")
    for dup in duplicates:
        print(f"Duplicate: {dup}")
