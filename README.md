# 📚 IndicPhotoOCR Project

This project performs **end-to-end Optical Character Recognition (OCR)** on natural scene images containing **Indic scripts**. It supports **text detection**, **script identification**, and **language-specific recognition**, producing structured outputs in **JSON** and **CSV** formats.

---

## 📁 Project Structure

```
IndicPhotoOCR-Project/
├── raw_images/              # Input images for OCR
├── ocr_outputs/             # Output JSON and CSV files
├── scripts/                 # Python scripts to run detection, script ID, and recognition
├── annotations/             # (Optional) Ground truth annotations for evaluation
├── requirements.txt         # Required Python packages
└── README.md                # Project overview and instructions
```

---

## 🚀 Features

- 🔍 **Text Detection** using [TextBPN++](https://github.com/hustvl/TextBPNPlusPlus)
- 🧠 **Script Identification** using Vision Transformer (ViT)-based models
- ✍️ **Text Recognition** using [PARseq](https://github.com/baudm/parseq)
- 💡 Outputs results in **JSON** and **CSV** formats
- 📊 Supports evaluation using ground-truth annotations

---

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/poireisoibam/IndicPhotoOCR-Project.git
cd IndicPhotoOCR-Project

# Create and activate a virtual environment (recommended)
conda create -n indicphotoocr python=3.10 -y
conda activate indicphotoocr

# Install all dependencies
pip install -r requirements.txt
```

---

## 🖼️ Usage

### Run OCR on all images in `raw_images/`:
```bash
python scripts/ocr.py
```

📁 Output files will be saved in the `ocr_outputs/` directory.

> ℹ️ For custom paths, batch size, or output format, edit `scripts/ocr.py` accordingly.

---

## 📦 Output Formats

### 🔸 JSON Format
```json
{
  "img_0": {
    "annotations": {
      "polygon_0": {
        "coordinates": [
          [45, 12], [180, 12], [180, 60], [45, 60]
        ],
        "text": "भारतीय",
        "script_language": "hindi"
      }
    }
  }
}
```

### 🔹 CSV Format

| image      | text     | bbox              | script_language |
|------------|----------|-------------------|------------------|
| IMG_1.JPG  | भारतीय   | [45, 12, 180, 60]  | hindi            |

---

## 📊 Evaluation

To evaluate the OCR performance using annotated ground-truth files:
```bash
python scripts/evaluation/wrr.py
```
Results (including per-language Word Recognition Rate or WRR) will be saved as a JSON summary in the `ocr_outputs/` directory.

---

## 🤝 Contribution to IndicPhotoOCR Benchmark

This dataset and evaluation framework were developed to enhance the **IndicPhotoOCR Benchmark**:  
🔗 [https://github.com/Bhashini-IITJ/IndicPhotoOCR](https://github.com/Bhashini-IITJ/IndicPhotoOCR)

---

## 🎓 Acknowledgement

This project was completed during a research internship under:

**Internship Supervisor**  
👨‍🏫 Prof. Anand Mishra  
Department of Computer Science & Engineering  
Indian Institute of Technology Jodhpur

**Internship Mentor**  
👨‍💻 Prof. Anik De  
Department of Computer Science & Engineering  
Indian Institute of Technology Jodhpur

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
