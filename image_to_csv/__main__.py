"""Main script to run the converter."""

import sys
from pathlib import Path

from .converter import ConverterFactory


def main() -> None:
    """Run the converter on all files in the input directory."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent

    # Define input and output directories
    input_dir = project_root / "input"
    output_dir = project_root / "output"

    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)

    # Process each file in the input directory
    for input_file in input_dir.glob("*"):
        if input_file.is_file():
            # Create output file path
            output_file = output_dir / f"{input_file.stem}.csv"

            # Create appropriate converter
            converter = ConverterFactory.create_converter(input_file, output_file)

            if converter:
                print(f"Converting {input_file.name}...")
                try:
                    converter.convert()
                    print(f"Successfully converted {input_file.name}")
                except Exception as e:
                    print(f"Error converting {input_file.name}: {str(e)}")
            else:
                print(f"Unsupported file type: {input_file.name}")


if __name__ == "__main__":
    main()
