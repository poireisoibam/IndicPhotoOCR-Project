import json
import os

# Paths to input files
gt_path = "annotations/annotations-files/Converted_json/converted_19_annotations.json" 
ocr_path = "ocr_outputs/ocr_combined_output_2.json"  

# Load ground truth
with open(gt_path, "r", encoding="utf-8") as f:
    gt_data = json.load(f)

# Load OCR result
with open(ocr_path, "r", encoding="utf-8") as f:
    ocr_data = json.load(f)

total_gt = 0
correct = 0

for image_name, gt_entry in gt_data.items():
    gt_annotations = gt_entry.get("annotations", {})
    ocr_annotations = ocr_data.get(image_name, {}).get("annotations", {})

    for idx, gt_poly in gt_annotations.items():
        gt_text = gt_poly.get("text", "").strip().lower()
        total_gt += 1

        # Try to match with OCR result for same polygon ID
        ocr_poly = ocr_annotations.get(idx)
        if ocr_poly:
            ocr_text = ocr_poly.get("text", "").strip().lower()
            if ocr_text == gt_text:
                correct += 1

# Calculate WRR
wrr = correct / total_gt if total_gt > 0 else 0

# Print result
print(f"✅ WRR (Word Recognition Rate): {wrr:.4f} ({correct}/{total_gt})")

# Save evaluation result
eval_output = {
    "total_ground_truth_words": total_gt,
    "correctly_recognized_words": correct,
    "wrr": round(wrr, 4)
}
with open("evaluation_result.json", "w", encoding="utf-8") as f:
    json.dump(eval_output, f, indent=2)

print("✅ Evaluation result saved to evaluation_result.json")

