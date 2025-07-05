import os
import cv2
import json
import numpy as np

def visualize_detection(image_path, detections, save_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f" Could not read image: {image_path}")
        return

    for item in detections:
        points = item.get("polygon") or item.get("points") or item.get("coordinates")
        text = item.get("text", "")
        lang = item.get("script") or item.get("lang") or item.get("script_language", "")

        # Convert [x1, y1, x2, y2] to box polygon
        if isinstance(points, list) and len(points) == 4 and isinstance(points[0], int):
            x1, y1, x2, y2 = points
            points = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]

        if not points or len(points) < 2:
            continue

        polygon = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
        cv2.polylines(image, [polygon], isClosed=True, color=(0, 255, 0), thickness=2)

        x, y = points[0]
        label = f"{text} ({lang})"
        cv2.putText(image, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    cv2.imwrite(save_path, image)
    print(f" Saved: {save_path}")


# === Paths ===
image_folder = "raw_images"  # your input image folder
json_path = "annotations/annotation-files/Converted_json/converted_annotations.json"  # detection results
output_folder = "outputs/visualized"

os.makedirs(output_folder, exist_ok=True)

# === Load JSON detections ===
with open(json_path, "r", encoding="utf-8") as f:
    all_detections = json.load(f)

# === Process each image ===
for image_id, data in all_detections.items():
    filename = f"{image_id}.jpg"  # or .png/.jpeg depending on your files
    image_path = os.path.join(image_folder, filename)

    if not os.path.exists(image_path):
        print(f" Image not found: {image_path}")
        continue

    detections = list(data.get("annotations", {}).values())
    save_path = os.path.join(output_folder, filename)
    visualize_detection(image_path, detections, save_path)
