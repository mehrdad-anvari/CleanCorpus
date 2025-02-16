import sys
from PIL import Image

def find(image_paths, min_width=None, min_height=None, max_width=None, max_height=None, min_aspect_ratio=None, max_aspect_ratio=None, exclude=True):
    """
    Filter images based on size and aspect ratio.

    Args:
        image_paths (list): List of image file paths.
        min_width (int): Minimum allowed width.
        min_height (int): Minimum allowed height.
        max_width (int): Maximum allowed width.
        max_height (int): Maximum allowed height.
        min_aspect_ratio (float): Minimum allowed aspect ratio (width/height).
        max_aspect_ratio (float): Maximum allowed aspect ratio (width/height).
        exclude (bool): If True, exclude images that don't meet the criteria. If False, include only those that do.

    Returns:
        list: Filtered list of image paths.
    """
    filtered_paths = []

    for image_path in image_paths:
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                aspect_ratio = width / height

                # Check size constraints
                size_valid = True
                if min_width is not None and width < min_width:
                    size_valid = False
                if min_height is not None and height < min_height:
                    size_valid = False
                if max_width is not None and width > max_width:
                    size_valid = False
                if max_height is not None and height > max_height:
                    size_valid = False

                # Check aspect ratio constraints
                aspect_ratio_valid = True
                if min_aspect_ratio is not None and aspect_ratio < min_aspect_ratio:
                    aspect_ratio_valid = False
                if max_aspect_ratio is not None and aspect_ratio > max_aspect_ratio:
                    aspect_ratio_valid = False

                # Apply exclusion logic
                if not exclude:
                    if size_valid and aspect_ratio_valid:
                        filtered_paths.append(image_path)
                else:
                    if not size_valid or not aspect_ratio_valid:
                        filtered_paths.append(image_path)

        except Exception as e:
            print(f"Skipping {image_path}: {e}", file=sys.stderr)

    return filtered_paths