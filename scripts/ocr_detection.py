import os
from IndicPhotoOCR.ocr import OCR

# Initialize OCR
ocr_system = OCR(verbose=True, device="cpu")

# Input image folder
folder = "raw_images"

# Output folder (same filenames will be used)
os.makedirs("outputs", exist_ok=True)

# Loop through all image files
for file in os.listdir(folder):
    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(folder, file)
        print(f"Processing {image_path}")
        
        # Run detection
        detections = ocr_system.detect(image_path)
        
        # Create output path using same filename
        output_path = os.path.join("detection_outputs", file)
        
        # Save visualized result
        ocr_system.visualize_detection(image_path, detections, save_path=output_path)
        print(f"Saved to: {output_path}")
