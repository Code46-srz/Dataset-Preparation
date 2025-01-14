import torch
import torch.nn.functional as F
import cv2
import os
import numpy as np

def ssim_pytorch(img1, img2, window_size=11, size_average=True):
    """Compute SSIM using PyTorch, GPU-accelerated."""
    img1 = torch.tensor(img1).float().unsqueeze(0).unsqueeze(0).cuda()
    img2 = torch.tensor(img2).float().unsqueeze(0).unsqueeze(0).cuda()

    # Gaussian kernel for smoothing
    window = torch.ones((1, 1, window_size, window_size)).cuda() / (window_size ** 2)
    mu1 = F.conv2d(img1, window, padding=window_size // 2, groups=1)
    mu2 = F.conv2d(img2, window, padding=window_size // 2, groups=1)

    mu1_sq = mu1.pow(2)
    mu2_sq = mu2.pow(2)
    mu1_mu2 = mu1 * mu2

    sigma1_sq = F.conv2d(img1 * img1, window, padding=window_size // 2, groups=1) - mu1_sq
    sigma2_sq = F.conv2d(img2 * img2, window, padding=window_size // 2, groups=1) - mu2_sq
    sigma12 = F.conv2d(img1 * img2, window, padding=window_size // 2, groups=1) - mu1_mu2

    C1 = 0.01 ** 2
    C2 = 0.03 ** 2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
    if size_average:
        return ssim_map.mean().item()
    else:
        return ssim_map.mean([1, 2, 3]).item()

def compare_images_in_folder(folder_path, threshold=0.95, delete_duplicates=False):
    """Compare images in a folder for similarity using SSIM."""
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    duplicates = []

    i = 0
    while i < len(files):
        file1 = files[i]
        if not os.path.exists(file1):
            # Skip if file has already been deleted
            i += 1
            continue
        
        for j in range(i + 1, len(files)):
            file2 = files[j]
            if not os.path.exists(file2):
                # Skip if file has already been deleted
                continue

            try:
                # Read images as grayscale
                img1 = cv2.imread(file1, cv2.IMREAD_GRAYSCALE)
                img2 = cv2.imread(file2, cv2.IMREAD_GRAYSCALE)

                if img1 is None or img2 is None:
                    print(f"Warning: One or both files could not be read: {file1}, {file2}")
                    continue

                # Resize images to the same size if needed
                if img1.shape != img2.shape:
                    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

                # Compute SSIM
                similarity = ssim_pytorch(img1, img2)
                if similarity >= threshold:
                    print(f"Similar images: {file1} and {file2} (SSIM: {similarity:.2f})")
                    duplicates.append((file1, file2))

                    if delete_duplicates:
                        print(f"Deleting: {file2}")
                        os.remove(file2)
                        files[j] = None  # Mark file as deleted
            except Exception as e:
                print(f"Error comparing {file1} and {file2}: {e}")

        i += 1

    # Remove any None entries left in the files list
    files = [f for f in files if f]

    return duplicates

# Example usage
if __name__ == "__main__":
    folder = "/home/virtual46/tool_tape_measure_images/"  # Replace with your image folder path
    threshold = 0.95  # Set your SSIM similarity threshold
    delete_duplicates = True  # Set to True to enable deletion of duplicates

    duplicates = compare_images_in_folder(folder, threshold=threshold, delete_duplicates=delete_duplicates)
    print("\nDetected duplicates:")
    for file1, file2 in duplicates:
        print(f"Duplicate pair: {file1}, {file2}")
