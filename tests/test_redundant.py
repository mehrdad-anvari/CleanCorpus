from pathlib import Path
from cleancorpus.filters import similar
from collections import Counter

# Sample test directory setup
TEST_IMAGE_DIR = Path("tests/test_images/set_1")


def extract_base_name(image_path: Path):
    """Extract base name without _similar or _duplicate suffixes."""
    return image_path.stem.rsplit("_", 1)[0] 


def test_find_similar_exclude():
    """Test that all redundant images are correctly excluded."""
    image_paths = set(TEST_IMAGE_DIR.glob("*.jpg"))

    filtered_images = set(similar.find(image_paths, hash_size=8, exclude=True))

    count_filtered_images = Counter([extract_base_name(p) for p in filtered_images])

    # Check that only one image from each group remains
    for N in count_filtered_images.values():
        assert N == 1, (
            f"Expected {N} to be equal to 1, but found more than one for a base name"
        )


def test_find_redundant_include():
    """Test that only redundant images remain when using 'include' action."""
    image_paths = set(TEST_IMAGE_DIR.glob("*.jpg"))

    filtered_images = set(similar.find(image_paths, hash_size=8, exclude=False))

    count_filtered_images = Counter([extract_base_name(p) for p in filtered_images])

    # Check that more than one image from each redundant group remains
    for N in count_filtered_images.values():
        assert N > 1, (
            f"Expected {N} to be greater than 1, but found only one or none for a base name"
        )
