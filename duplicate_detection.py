import os
import hashlib
from PIL import Image
import imagehash

def remove_exact_duplicates(folder_path):
    """Remove exact duplicates (byte-for-byte identical files)."""
    hash_map = {}
    duplicates = []
    
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
            if file_hash in hash_map:
                print(f"Exact duplicate found: {file_path} (original: {hash_map[file_hash]})")
                duplicates.append(file_path)
                os.remove(file_path)  # Remove the duplicate
            else:
                hash_map[file_hash] = file_path
    
    print(f"Removed {len(duplicates)} exact duplicates")
    return duplicates

def find_near_duplicates(folder_path, threshold=5):
    """Identify near-duplicates based on perceptual hashing."""
    hash_map = {}
    duplicates = []
    
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            try:
                image = Image.open(file_path)
                img_hash = imagehash.average_hash(image)
                for existing_hash, existing_path in hash_map.items():
                    if img_hash - existing_hash < threshold:  # Lower threshold = stricter match
                        print(f"Near-duplicate found: {file_path} is similar to {existing_path}")
                        duplicates.append((file_path, existing_path))
                        break
                else:
                    hash_map[img_hash] = file_path
            except Exception as e:
                print(f"Error processing file '{file_path}': {e}")
    
    print(f"Found {len(duplicates)} near-duplicates")
    return duplicates

# Example usage
if __name__ == "__main__":
    folder = "path/to/images"  # Replace with your folder path

    # Step 1: Remove exact duplicates
    remove_exact_duplicates(folder)

    # Step 2: Detect near-duplicates
    near_duplicates = find_near_duplicates(folder)
    for file, similar_file in near_duplicates:
        print(f"Near-duplicate pair: {file} and {similar_file}")
