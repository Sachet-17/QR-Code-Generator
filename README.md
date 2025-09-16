# QR Code Generator (Tkinter)

A tiny desktop app to turn any link into a crisp QR code you can preview and save as a JPEG.

Web version: 👉 **Live demo:** https://sachet-17.github.io/QR-Code-Generator/

## Features
- 🔗 Smart URL handling (auto-adds `https://` if missing)
- 🧾 Clean filenames (`qr_<host>.jpg`)
- 🖼️ Live preview (500×500 pane)
- 💾 High-quality JPEG export (RGB, quality=95, optimized)
- ⌨️ Press **Enter** to Generate

## Requirements
- Python **3.8+** (3.10+ recommended)
- **Tkinter** (usually included with Python)
  - Linux users may need:  
    ```bash
    sudo apt install python3-tk
    ```
- Pip packages:  
  - `qrcode[pil]`  
  - `Pillow`

## Installation
```bash
# 1. Clone or copy this repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# 2. (Optional) Create a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install "qrcode[pil]" Pillow
