import matplotlib.pyplot as plt
import numpy as np


def apply_mask(image, mask, mask_color=(0, 0, 0)):
    if mask == None:
        return image
    # Ensure the mask is boolean
    mask = mask.astype(bool)

    # Initialize the masked image as a copy of the original
    masked_image = np.copy(image)

    # Apply the mask
    if image.ndim == 3:  # RGB image
        # Create a mask with the same shape as the image
        color_mask = np.array(mask_color).reshape((1, 1, 3))
        masked_image[mask] = color_mask
    else:  # Grayscale image
        masked_image[mask] = mask_color[0]  # Use the first channel for grayscale

    return masked_image


if __name__ == "__main__":
    # Example usage
    # Generate a random image and mask for demonstration
    image = np.random.rand(100, 100, 3)  # Random RGB image
    mask = np.random.randint(0, 2, (100, 100), dtype=bool)  # Random mask with 0s and 1s

    # Apply the mask
    masked_image = apply_mask(image, mask)

    # Display the original and masked images
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.title("Original Image")
    plt.imshow(image)

    plt.subplot(1, 2, 2)
    plt.title("Masked Image")
    plt.imshow(masked_image)

    plt.show()
