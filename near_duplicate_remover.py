from PIL import Image
import imagehash
import os

def find_near_duplicates(folder_path, threshold=5):
    hash_map = {}
    duplicates = []
    
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            try:
                # Calculate perceptual hash
                image = Image.open(file_path)
                img_hash = imagehash.average_hash(image)
                
                # Compare with existing hashes
                for existing_hash, existing_path in hash_map.items():
                    if img_hash - existing_hash < threshold:  # Lower threshold = stricter match
                        print(f"Similar: {file_path} is similar to {existing_path}")
                        duplicates.append((file_path, existing_path))
                        break
                else:
                    hash_map[img_hash] = file_path
            except Exception as e:
                print(f"Error processing file '{file_path}': {e}")
    
    print(f"Found {len(duplicates)} similar images")
    return duplicates

# Example usage
folder = ""  # Ensure this path is correct
duplicates = find_near_duplicates(folder)
