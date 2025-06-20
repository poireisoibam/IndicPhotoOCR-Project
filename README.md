# IndicPhotoOCR Project

This project performs end-to-end Optical Character Recognition (OCR) on natural scene images containing Indic scripts. It supports detection, script identification, and text recognition.

## 📁 Project Structure

```
IndicPhotoOCR-Project/
├── raw_images/              # Input images for OCR
├── ocr_outputs/             # JSON and CSV outputs
├── scripts/                 # Python scripts for running OCR
├── annotations/             # (Optional) Annotation files
├── requirements.txt         # Python dependencies
└── README.md                # Project overview
```

## 🚀 Features

- Text detection using `TextBPN++`
- Script identification using ViT-based models
- Script-specific recognition using `PARseq`
- Output in JSON or CSV formats

## 🔧 Installation

```bash
# Clone the repo
git clone https://github.com/poireisoibam/IndicPhotoOCR-Project.git
cd IndicPhotoOCR-Project

# Set up virtual environment (recommended)
conda create -n indicphotoocr python=3.10 -y
conda activate indicphotoocr

# Install dependencies
pip install -r requirements.txt
```

## 🖼️ Usage

### Run OCR on a single image:
```bash
python scripts/test_ocr_5.py
```

### Run OCR on a folder of images:
```bash
python scripts/test_ocr.py
```

## 📦 Output Format

### JSON (example):
```json
{
  "img_0": {
    "txt": "भारतीय",
    "bbox": [45, 12, 180, 60]
  }
}
```

### CSV (example):
| image       | text     | bbox             |
|-------------|----------|------------------|
| IMG_1.JPG   | भारतीय   | [45, 12, 180, 60] |

## 📜 License

[MIT License](LICENSE)
