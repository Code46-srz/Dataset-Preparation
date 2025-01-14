from skimage.metrics import structural_similarity as ssim
import cv2
import os

def compare_images_ssim(image1_path, image2_path):
    """Compare two images using SSIM."""
    image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    # Resize images to the same size if needed
    if image1.shape != image2.shape:
        image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

    # Compute SSIM
    score, _ = ssim(image1, image2, full=True)
    return score

def find_duplicates_ssim(folder_path, threshold=0.95):
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    duplicates = []

    for i, file1 in enumerate(files):
        for file2 in files[i + 1:]:
            try:
                similarity = compare_images_ssim(file1, file2)
                if similarity >= threshold:
                    print(f"Similar images: {file1} and {file2} (SSIM: {similarity:.2f})")
                    duplicates.append((file1, file2))
            except Exception as e:
                print(f"Error comparing {file1} and {file2}: {e}")

    return duplicates

# Example usage
folder = "path/to/images"# Replace with your image folder path
similar_images = find_duplicates_ssim(folder)
for img1, img2 in similar_images:
    print(f"Duplicate pair: {img1}, {img2}")
