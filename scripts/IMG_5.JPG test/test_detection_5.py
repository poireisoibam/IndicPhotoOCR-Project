from IndicPhotoOCR.ocr import OCR
# Create an object of OCR
ocr_system = OCR(verbose=True) # for CPU --> OCR(device="cpu")

# Get detections
detections = ocr_system.detect("test_images/image_141.jpg")

# Running text detection...
# 4334 text boxes before nms
# 1.027989387512207

# Save and visualize the detection results
ocr_system.visualize_detection("test_images/image_141.jpg", detections)
# Image saved at: test.png
