import os
import json
from IndicPhotoOCR.ocr import OCR

# Define input image folder and output path
image_folder = "raw_images"
output_path = "ocr_outputs"
combined_json_path = os.path.join(output_path, "ocr_combined_output.json")
os.makedirs(output_path, exist_ok=True)

# Create OCR object
ocr_system = OCR(verbose=True, identifier_lang="auto", device="cpu")

# Supported image extensions
valid_exts = (".jpg", ".jpeg", ".png")

# Dictionary to hold results
all_results = {}

# Process each image
for filename in os.listdir(image_folder):
    if filename.lower().endswith(valid_exts):
        image_path = os.path.join(image_folder, filename)
        print(f"\nProcessing: {image_path}")

        try:
            result = ocr_system.ocr(image_path)
            all_results[filename] = result
        except Exception as e:
            print(f" Failed on {filename}: {e}")
            continue

# Save combined results
with open(combined_json_path, "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

print(f"\n Combined OCR results saved to: {combined_json_path}")

