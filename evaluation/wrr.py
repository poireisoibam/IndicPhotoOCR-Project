import json

# === File paths ===
gt_path = "annotations/annotations-files/Converted_json/converted_annotations.json"  # your GT file
ocr_path = "ocr_outputs/ocr_combined_output_poly.json"  # your OCR file
output_path = "evaluation_result.json"

# === Load files ===
with open(gt_path, "r", encoding="utf-8") as f:
    gt_data = json.load(f)

with open(ocr_path, "r", encoding="utf-8") as f:
    ocr_data = json.load(f)

# === Evaluation counters ===
total_gt = 0
correct = 0

for image_name, gt_entry in gt_data.items():
    gt_annotations = list(gt_entry.get("annotations", {}).values())
    ocr_annotations = list(ocr_data.get(image_name, {}).get("annotations", {}).values())

    # Create a pool of (text, lang) from OCR entries
    ocr_pool = [
        (
            ocr_ann.get("text", "").strip().lower(),
            ocr_ann.get("script_language", "").strip().lower()
        )
        for ocr_ann in ocr_annotations
    ]

    for gt_ann in gt_annotations:
        gt_text = gt_ann.get("text", "").strip().lower()
        gt_lang = gt_ann.get("script_language", "").strip().lower()
        total_gt += 1

        if (gt_text, gt_lang) in ocr_pool:
            correct += 1

# === Final WRR ===
wrr = correct / total_gt if total_gt > 0 else 0
result = {
    "total_ground_truth_words": total_gt,
    "correctly_recognized_words": correct,
    "wrr_case_insensitive": round(wrr, 4)
}

# === Save to file ===
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

print(f" WRR: {wrr:.4f} ({correct}/{total_gt})")
print(f" Saved to {output_path}")
