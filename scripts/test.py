from IndicPhotoOCR.ocr import OCR
ocr_system = OCR(verbose=True, identifier_lang="auto", device="cpu")
ocr_system.ocr("raw_images/sample.jpg")
