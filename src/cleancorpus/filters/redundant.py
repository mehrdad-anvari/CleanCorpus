import sys
import imagehash
from PIL import Image
from collections import defaultdict

def find(image_paths, hash_size=8, include=False):
    """Filter redundant images (either keeping or removing them)."""
    hashes = defaultdict(list)
    for image_path in image_paths:
        try:
            with Image.open(image_path) as img:
                img_hash = imagehash.average_hash(img, hash_size=hash_size)
                hashes[img_hash].append(image_path)
        except Exception as e:
            print(f"Skipping {image_path}: {e}", file=sys.stderr)

    # Filter paths based on similarity and exclusion logic
    filtered_paths = []
    for paths in hashes.values():
        if include:
            # print(paths[0])  
            filtered_paths.append(paths[0])
        elif len(paths) > 1:  
            filtered_paths.extend(paths[1:])

    return filtered_paths