import json
import unicodedata
import string
import csv
from collections import defaultdict
from difflib import SequenceMatcher

# ---------- Normalization helpers ----------
def normalize_english(word: str) -> str:
    word = word.lower().strip()
    word = word.translate(str.maketrans('', '', string.punctuation))
    return word

def normalize_hindi(word: str) -> str:
    word = unicodedata.normalize("NFC", word.strip())
    word = word.replace("ड़", "ड").replace("ढ़", "ढ")  # simplify nukta
    return word

def fix_language(script, text):
    script = script.lower()
    if script == "marathi" and any("\u0900" <= ch <= "\u097F" for ch in text):
        return "hindi"
    if script in ["english", "eng", "en"]:
        return "english"
    return script

def is_match(gt, pred):
    if gt == pred:
        return True
    return SequenceMatcher(None, gt, pred).ratio() >= 0.7

# ---------- Load files ----------
with open("converted_annotations.json", "r", encoding="utf-8") as f:
    gt_data = json.load(f)

with open("ocr_combined_output_poly.json", "r", encoding="utf-8") as f:
    pred_data = json.load(f)

# ---------- Flatten ground truth ----------
ground_truth = []
for img, ann in gt_data.items():
    blocks = ann.get("annotations", ann)
    for poly, details in blocks.items():
        text = details["text"]
        script = details["script_language"].lower()
        norm_text = normalize_english(text) if script == "english" else normalize_hindi(text)
        ground_truth.append((img, norm_text, script))

# ---------- Flatten predictions ----------
predictions = defaultdict(list)
for img, ann in pred_data.items():
    blocks = ann.get("annotations", ann)
    for poly, details in blocks.items():
        text = details["text"]
        script = fix_language(details["script_language"], text)
        if script == "english":
            text = normalize_english(text)
        elif script == "hindi":
            text = normalize_hindi(text)
        predictions[img].append((text, script))

# ---------- Evaluate ----------
lang_stats = defaultdict(lambda: {"total": 0, "correct": 0})

for img, gt_text, gt_lang in ground_truth:
    lang_stats[gt_lang]["total"] += 1
    if img in predictions:
        for pred_text, pred_lang in predictions[img]:
            if pred_lang == gt_lang and is_match(gt_text, pred_text):
                lang_stats[gt_lang]["correct"] += 1
                break

# ---------- Compute WRR ----------
results = {}
overall_total = 0
overall_correct = 0
for lang, stats in lang_stats.items():
    total = stats["total"]
    correct = stats["correct"]
    wrr = correct / total if total > 0 else 0
    results[lang] = {"total": total, "correct": correct, "wrr": round(wrr, 4)}
    overall_total += total
    overall_correct += correct

results["overall"] = {
    "total": overall_total,
    "correct": overall_correct,
    "wrr": round(overall_correct / overall_total, 4) if overall_total > 0 else 0
}

# ---------- Print Results ----------
print("\n==== Word Recognition Rate (WRR) Results ====\n")
for lang, stats in results.items():
    print(f"{lang:10} | total: {stats['total']:4d} | correct: {stats['correct']:4d} | wrr: {stats['wrr']:.4f}")

# ---------- Save to CSV ----------
with open("wrr_results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["language", "total", "correct", "wrr"])
    for lang, stats in results.items():
        writer.writerow([lang, stats["total"], stats["correct"], stats["wrr"]])

print("\n WRR results saved to wrr_results.csv")
