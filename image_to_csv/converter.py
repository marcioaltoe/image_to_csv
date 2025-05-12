"""Core conversion functionality."""

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Dict, Any
import re

import cv2
import numpy as np
import pandas as pd
from pdf2image import convert_from_path
from PIL import Image
import pytesseract


class FileConverter(ABC):
    """Abstract base class for file converters."""

    def __init__(self, input_path: Path, output_path: Path):
        """Initialize the converter.

        Args:
            input_path: Path to the input file
            output_path: Path to save the output file
        """
        self.input_path = input_path
        self.output_path = output_path

    @abstractmethod
    def convert(self) -> None:
        """Convert the input file to CSV."""
        pass

    def _process_text_to_dataframe(self, text: str) -> pd.DataFrame:
        """Process extracted text into a DataFrame.

        Args:
            text: Extracted text from the document

        Returns:
            DataFrame containing the processed data
        """
        # Split text into lines and remove empty lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        # Remove header noise and empty lines
        lines = [line for line in lines if not line.startswith('a ane em lI Ni NR')]

        # Process each line to extract fields
        processed_data = []
        for line in lines:
            # Skip lines that are just noise or separators
            if line in ['—_— apace,', ''] or line.startswith('—_—'):
                continue

            # Try to extract fields using regex patterns
            # Pattern for NFe data: chave, documento, numero, data, situacao
            pattern = r'(\d{44})\s+(\d{14})\s+(\d+)\s+(\d{2}/\d{2}/\d{4})\s+(Aprovado)'
            match = re.search(pattern, line)

            if match:
                chave, documento, numero, data, situacao = match.groups()
                processed_data.append([chave, documento, numero, data, situacao])
            else:
                # If regex doesn't match, try to split by multiple spaces
                fields = re.split(r'\s{2,}', line)
                # Clean up fields
                fields = [field.strip() for field in fields if field.strip()]
                if fields:
                    processed_data.append(fields)

        if not processed_data:
            return pd.DataFrame()

        # Convert to DataFrame
        df = pd.DataFrame(processed_data)

        # If we have the expected number of columns, name them
        if len(df.columns) == 5:
            df.columns = ['Chave de Acesso', 'Documento', 'Número', 'Data', 'Situação']

        # Clean up the DataFrame
        df = df.replace('', np.nan).dropna(how='all', axis=1)

        return df

    def _enhance_image_for_ocr(self, image: Image.Image) -> Image.Image:
        """Enhance image for better OCR results.

        Args:
            image: Input image

        Returns:
            Enhanced image
        """
        # Convert PIL Image to OpenCV format
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to preprocess the image
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Apply dilation to connect text components
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        gray = cv2.dilate(gray, kernel, iterations=1)

        # Convert back to PIL Image
        return Image.fromarray(gray)


class PDFConverter(FileConverter):
    """Convert PDF files to CSV."""

    def convert(self) -> None:
        """Convert PDF to CSV using OCR."""
        # Convert PDF to images
        pages = convert_from_path(str(self.input_path), dpi=300)

        # Process each page
        for i, page in enumerate(pages, start=1):
            # Enhance image for better OCR
            enhanced_page = self._enhance_image_for_ocr(page)

            # Perform OCR with custom configuration
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(enhanced_page, config=custom_config)

            # Process text to DataFrame
            df = self._process_text_to_dataframe(text)

            if not df.empty:
                # Save to CSV
                output_file = self.output_path.parent / f"{self.output_path.stem}_page{i}.csv"
                df.to_csv(output_file, index=False, sep=',', quoting=1)  # quoting=1 for CSV.QUOTE_ALL


class ImageConverter(FileConverter):
    """Convert image files to CSV."""

    def convert(self) -> None:
        """Convert image to CSV using OCR."""
        # Open and enhance image
        img = Image.open(self.input_path)
        enhanced_img = self._enhance_image_for_ocr(img)

        # Perform OCR with custom configuration
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(enhanced_img, config=custom_config)

        # Process text to DataFrame
        df = self._process_text_to_dataframe(text)

        if not df.empty:
            # Save to CSV
            df.to_csv(self.output_path, index=False, sep=',', quoting=1)  # quoting=1 for CSV.QUOTE_ALL


class ConverterFactory:
    """Factory for creating appropriate converters."""

    @staticmethod
    def create_converter(input_path: Path, output_path: Path) -> Optional[FileConverter]:
        """Create appropriate converter based on file extension.

        Args:
            input_path: Path to the input file
            output_path: Path to save the output file

        Returns:
            Appropriate converter instance or None if file type not supported
        """
        extension = input_path.suffix.lower()

        if extension == ".pdf":
            return PDFConverter(input_path, output_path)
        elif extension in [".jpg", ".jpeg", ".png"]:
            return ImageConverter(input_path, output_path)

        return None
