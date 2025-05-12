# Image to CSV Converter

A Python tool that converts PDF and image files (JPG, PNG) to CSV format using OCR (Optical Character Recognition). This tool is particularly useful for extracting tabular data from documents and images.

## Features

- Convert PDF files to CSV
- Convert image files (JPG, PNG) to CSV
- Automatic table detection and extraction
- Image enhancement for better OCR results
- Support for multi-page PDFs
- Clean and organized output in CSV format

## Prerequisites

- Python 3.8 or higher
- Tesseract OCR installed on your system

### Installing Tesseract OCR

#### macOS

```bash
brew install tesseract
```

#### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

#### Windows

1. Download the installer from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer
3. Add Tesseract to your system PATH

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/image-to-csv.git
cd image-to-csv
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

3. Install dependencies:

```bash
pip install -e .
```

## Usage

1. Place your PDF or image files in the `input` directory
2. Run the converter:

```bash
python -m image_to_csv
```

3. Find the converted CSV files in the `output` directory

### File Naming Convention

- For PDFs: `{original_name}_page{page_number}.csv`
- For images: `{original_name}.csv`

## How It Works

1. **PDF Processing**:

   - Converts PDF pages to images
   - Enhances image quality for better OCR
   - Performs OCR on each page
   - Detects and extracts tabular data
   - Saves each page as a separate CSV file

2. **Image Processing**:
   - Enhances image quality
   - Performs OCR
   - Detects and extracts tabular data
   - Saves as CSV file

## Project Structure

```
image-to-csv/
├── input/          # Input directory for PDF and image files
├── output/         # Output directory for CSV files
├── image_to_csv/   # Source code
│   ├── __init__.py
│   ├── __main__.py
│   └── converter.py
├── pyproject.toml  # Project configuration
└── README.md       # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [pdf2image](https://github.com/Belval/pdf2image)
- [OpenCV](https://opencv.org/)
- [Pillow](https://python-pillow.org/)
