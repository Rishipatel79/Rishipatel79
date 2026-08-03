from rembg import remove
from PIL import Image
import cv2
import numpy as np
import os

# Input and output paths
INPUT_IMAGE = "assets/source-photo.jpg"
OUTPUT_IMAGE = "assets/source-prepped.png"

print("Loading image...")

# Load image
image = Image.open(INPUT_IMAGE)

# Remove background
print("Removing background...")
image = remove(image)

# Convert to OpenCV format
image = np.array(image)

# Separate alpha channel
alpha = image[:, :, 3]
rgb = image[:, :, :3]

# White background
white = np.ones_like(rgb) * 255

mask = alpha / 255.0

for c in range(3):
    white[:, :, c] = rgb[:, :, c] * mask + white[:, :, c] * (1 - mask)

# Convert to grayscale
gray = cv2.cvtColor(white.astype(np.uint8), cv2.COLOR_RGB2GRAY)

# Improve contrast using CLAHE
clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
gray = clahe.apply(gray)

# Save output
cv2.imwrite(OUTPUT_IMAGE, gray)

print("Done!")
print("Saved:", OUTPUT_IMAGE)