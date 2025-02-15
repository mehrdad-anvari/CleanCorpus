import sys
import imagehash
from PIL import Image
from collections import defaultdict

def find(image_paths, hash_size=8, exclude=True):
    """Filter similar images (either keeping or removing them)."""
    hashes = defaultdict(list)
    for image_path in image_paths:
        try:
            with Image.open(image_path) as img:
                img_hash = imagehash.average_hash(img, hash_size=hash_size)
                hashes[img_hash].append(image_path)
        except Exception as e:
            print(f"Skipping {image_path}: {e}", file=sys.stderr)

    if exclude:
        return [paths[0] for paths in hashes.values()]  # Keep only unique images
    else:
        return [p for paths in hashes.values() if len(paths) > 1 for p in paths]  # Keep only duplicates