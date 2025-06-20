from IndicPhotoOCR.ocr import OCR
import json

# Create an object of OCR
ocr_system = OCR(verbose=True, identifier_lang ="auto", device="cpu")

# Complete pipeline
ocr_system.ocr("raw_image/IMG_5.JPG")

results = ocr_system.ocr("raw_image/IMG_5.JPG")

with open("ocr_output.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
