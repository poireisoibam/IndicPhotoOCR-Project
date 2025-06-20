from IndicPhotoOCR.ocr import OCR
import os
import json

# Fix for OpenMP issue
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Create OCR object
ocr_system = OCR(verbose=True, device="cpu")

# Path to image
image_path = "raw_images/IMG_5.JPG"
image_filename = os.path.basename(image_path)

# Run detection
detections = ocr_system.detect(image_path)

# Visualize detections
ocr_system.visualize_detection(image_path, detections)

# Run recognition (change "hindi" if needed)
recognized = ocr_system.recogniser.recognise(
    "hindi",
    "raw_images/IMG_5.JPG",
    detections,
    "hindi",
    True,
    "cpu"
)

# Save recognized words to JSON
output_data = {image_filename: recognized}

with open("output_text.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

print("Saved to output_text.json")

