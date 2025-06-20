import os
import json
import csv
from IndicPhotoOCR.ocr import OCR

image_folder = "raw_images"
output_folder = "ocr_outputs"
os.makedirs(output_folder, exist_ok=True)

ocr_system = OCR(verbose=True, identifier_lang="auto", device="cpu")
valid_exts = (".jpg", ".jpeg", ".png")

csv_path = os.path.join(output_folder, "ocr_results.csv")
with open(csv_path, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["image", "text", "bbox"])

    for filename in os.listdir(image_folder):
        if filename.lower().endswith(valid_exts):
            image_path = os.path.join(image_folder, filename)
            print(f"Processing: {image_path}")

            try:
                result = ocr_system.ocr(image_path)
            except Exception as e:
                print(f" Failed on {filename}: {e}")
                continue

            json_name = os.path.splitext(filename)[0] + ".json"
            json_path = os.path.join(output_folder, json_name)
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            if isinstance(result, dict):
                for key, value in result.items():
                    text = value.get("txt", "").replace("\n", " ")
                    bbox = value.get("bbox", [])
                    writer.writerow([filename, text, bbox])
            else:
                print(f" Skipping {filename}: OCR returned non-dict result")

print(f" CSV saved to: {csv_path}")
