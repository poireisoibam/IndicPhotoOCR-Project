import os
import csv
from IndicPhotoOCR.ocr import OCR

# Paths
image_folder = "raw_images"
output_csv = "ocr_outputs/ocr_combined_output.csv"
os.makedirs("ocr_outputs", exist_ok=True)

# OCR setup
ocr_system = OCR(verbose=True, identifier_lang="auto", device="cpu")
valid_exts = (".jpg", ".jpeg", ".png")

# CSV export
with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["image_id", "polygon_id", "x1", "y1", "x2", "y2", "text", "script_language"])

    for filename in os.listdir(image_folder):
        if not filename.lower().endswith(valid_exts):
            continue

        image_path = os.path.join(image_folder, filename)
        image_id = os.path.splitext(filename)[0]
        print(f"\n📷 Processing: {filename}")

        try:
            result = ocr_system.ocr(image_path)
        except Exception as e:
            print(f"❌ Failed on {filename}: {e}")
            continue

        if not isinstance(result, dict):
            print(f"⚠️ Skipping {filename}: OCR did not return a dict")
            continue

        for polygon_id, polygon_data in result.items():
            try:
                coords = polygon_data.get("coordinates", [])
                text = polygon_data.get("text", "")
                script = polygon_data.get("script_language", "unknown")

                if len(coords) == 4:
                    x1, y1, x2, y2 = coords
                else:
                    x1 = y1 = x2 = y2 = ""

                writer.writerow([image_id, polygon_id, x1, y1, x2, y2, text, script])

            except Exception as e:
                print(f"⚠️ Error in polygon {polygon_id} of {filename}: {e}")

print(f"\n✅ CSV saved at: {output_csv}")

