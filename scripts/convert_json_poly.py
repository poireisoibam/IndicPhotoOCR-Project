import json

def convert_via_to_custom_format(via_json_path, output_path):
    with open(via_json_path, 'r') as f:
        data = json.load(f)

    output = {}

    for entry in data.values():
        filename = entry.get("filename", "")
        image_id = filename.rsplit('.', 1)[0]  # e.g., "IMG_10"

        regions = entry.get("regions", [])
        annotations = {}

        for i, region in enumerate(regions):
            shape = region.get("shape_attributes", {})
            attrs = region.get("region_attributes", {})

            x_points = shape.get("all_points_x", [])
            y_points = shape.get("all_points_y", [])
            coordinates = [[x, y] for x, y in zip(x_points, y_points)]

            annotations[f"polygon_{i}"] = {
                "coordinates": coordinates,
                "text": attrs.get("text", ""),
                "script_language": attrs.get("lang", "")
            }

        output[image_id] = {
            "annotations": annotations
        }

    with open(output_path, 'w') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f"Converted {len(output)} images. Saved to: {output_path}")

# Usage
convert_via_to_custom_format("via_project_31_json.json", "via_project_31_custom_polygons.json")
