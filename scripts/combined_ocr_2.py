import os
import json
from IndicPhotoOCR.ocr import OCR

# Folder settings
image_folder = "raw_images"
output_path = "ocr_outputs"
combined_json_path = os.path.join(output_path, "ocr_combined_output_2.json")
os.makedirs(output_path, exist_ok=True)

# OCR object
ocr_system = OCR(verbose=True, identifier_lang="auto", device="cpu")
valid_exts = (".jpg", ".jpeg", ".png")

# Final JSON
final_results = {}

for filename in os.listdir(image_folder):
    if filename.lower().endswith(valid_exts):
        image_path = os.path.join(image_folder, filename)
        print(f"\n📷 Processing: {image_path}")
        
        try:
            results = ocr_system.ocr(image_path)
        except Exception as e:
            print(f"❌ Failed on {filename}: {e}")
            continue

        # Create structure
        image_id = os.path.splitext(filename)[0]
        final_results[image_id] = {"annotations": {}}

        if isinstance(results, dict):
            for idx, (key, item) in enumerate(results.items()):
                if not isinstance(item, dict):
                    print(f"⚠️ Skipping polygon {idx} in {filename}: Not a dict")
                    continue

                coords = item.get("coordinates")
                if not coords:
                    print(f"⚠️ No coordinates in polygon {idx} of {filename}")
                    continue

                try:
                    polygon = {
                        "coordinates": coords,
                        "text": item["text"],
                        "script_language": item.get("script_language", "unknown")
                    }
                    final_results[image_id]["annotations"][f"polygon_{idx}"] = polygon
                except Exception as e:
                    print(f"⚠️ Error in polygon {idx} of {filename}: {e}")
        else:
            print(f"⚠️ Skipping {filename}: OCR did not return a dict")


# Save JSON
with open(combined_json_path, "w", encoding="utf-8") as f:
    json.dump(final_results, f, ensure_ascii=False, indent=2)

print(f"\n✅ Output saved to: {combined_json_path}")
