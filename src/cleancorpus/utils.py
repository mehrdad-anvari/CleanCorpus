import sys
from pathlib import Path
from typing import List

def read_input() -> List[Path]:
    """Reads file paths from stdin or returns provided arguments.
    
    Returns:
        List[Path]: A list of file paths read from stdin.
    """
    if not sys.stdin.isatty():  # If data is piped
        return [Path(line.strip()) for line in sys.stdin]
    return []

def copy_images(image_paths: List[Path], output_dir: str) -> List[Path]:
    """Copy selected images to an output directory.

    Args:
        image_paths (List[Path]): List of image file paths to be copied.
        output_dir (str): The destination directory where images will be copied.

    Returns:
        List[Path]: The list of copied image paths for further processing.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for img_path in image_paths:
        destination = output_dir / img_path.name
        print(f"Copying {img_path} to {destination}", file=sys.stderr)
        destination.write_bytes(img_path.read_bytes())

    return image_paths  # Output paths for further processing
