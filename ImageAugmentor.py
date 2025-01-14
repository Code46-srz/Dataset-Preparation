import os
import hashlib
import random
import cv2
import albumentations as A

class ImageAugmentor:
    """
    A class for augmenting images and managing variations.

    Attributes:
        folder_path (str): Path to the folder containing original images.
        save_dir (str): Directory where augmented images will be saved, set to 1 to save in same folder_path.
    """
    def __init__(self, folder_path, save_dir):
        self.folder_path = folder_path
        self.save_dir = save_dir
        #if save_dir = 1, the files will be saved into the folder_path directory
        if self.save_dir == 1:
            self.save_dir = self.folder_path
            os.makedirs(self.save_dir, exist_ok=True) 

    def augment_image(self, image_path, num_variations=3):
        """Augment a single image and save variations."""
        # Ensure the image exists
        if not os.path.exists(image_path):
            print(f"Error: Image '{image_path}' does not exist.")
            return

        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to read the image: {image_path}")
            return

            # Updated augmentation pipeline
        transform = A.Compose([
             A.PadIfNeeded(min_height=512, min_width=512, border_mode=cv2.BORDER_CONSTANT, p=1.0),
             A.HorizontalFlip(p=0.5),
             A.Rotate(limit=15, p=0.5),
             A.RandomBrightnessContrast(p=0.5),
             A.GaussianBlur(blur_limit=(3, 7), p=0.3),
             A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.1, rotate_limit=10, p=0.5),
        ])


        # Generate augmented images
        base_filename = os.path.splitext(os.path.basename(image_path))[0]
        for i in range(1, num_variations + 1):
            augmented = transform(image=image)['image']
            augmented_filename = f"{base_filename}_var{i}.jpg"
            augmented_path = os.path.join(self.save_dir, augmented_filename)
            cv2.imwrite(augmented_path, augmented)
            print(f"Augmented image saved to: {augmented_path}")

    def augment_random_images(self, num_images=5, num_variations=3):
        """Augment a random selection of images."""
        # Ensure the folder exists
        if not os.path.exists(self.folder_path):
            print(f"Error: Folder '{self.folder_path}' does not exist.")
            return

        # List all image files in the folder
        image_files = [os.path.join(self.folder_path, f) for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]
        if len(image_files) == 0:
            print("No images found in the folder.")
            return

        # Select random images
        selected_images = random.sample(image_files, min(num_images, len(image_files)))
        print(f"Selected images: {selected_images}")

        # Augment each selected image
        for image_path in selected_images:
            self.augment_image(image_path, num_variations=num_variations)

# Example usage
if __name__ == "__main__":
    folder = "path/to/folder"  # Path to the folder containing images
    save_dir = 1  # Directory to save augmented images

    augmentor = ImageAugmentor(folder, save_dir)

    # Augment a specific image
    image_path = "path/to/folder"  # Replace with your image file
    augmentor.augment_image(image_path, num_variations=8)

    # Augment random images
    #augmentor.augment_random_images(num_images=10, num_variations=3)

    
    
    #Todo: implement a way to better way to agument based on result of number of files based on clean up
