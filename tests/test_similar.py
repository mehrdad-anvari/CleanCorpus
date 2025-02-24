from pathlib import Path
from cleancorpus.filters import similar

# Sample test directory setup
TEST_IMAGE_DIR = Path("tests/test_images/set_1")


def extract_base_name(image_path: Path):
    """Extract base name without _similar or _duplicate suffixes."""
    return image_path.stem.rsplit("_", 1)[0] 


def test_find_similar_exclude():
    """Test that duplicate and similar images are correctly excluded."""
    image_paths = set(TEST_IMAGE_DIR.glob("*.jpg"))
    duplicate_images = set(TEST_IMAGE_DIR.glob("*_duplicate.jpg"))
    similar_images = set(TEST_IMAGE_DIR.glob("*_similar.jpg"))
    original_images = set(TEST_IMAGE_DIR.glob("*_original.jpg"))

    filtered_images = set(similar.find(image_paths, hash_size=8, exclude=True))

    # Extract base names of all non-unique images
    not_unique_bases = {extract_base_name(p) for p in (similar_images | duplicate_images)}

    # Identify unique original images (those that don't have a similar/duplicate counterpart)
    expected_remaining = {p for p in original_images if extract_base_name(p) not in not_unique_bases}

    assert filtered_images == expected_remaining, (
        f"Expected {expected_remaining}, but got {filtered_images}"
    )


def test_find_similar_include():
    """Test that only similar and duplicate images remain when using 'include' action."""
    image_paths = set(TEST_IMAGE_DIR.glob("*.jpg"))
    duplicate_images = set(TEST_IMAGE_DIR.glob("*_duplicate.jpg"))
    similar_images = set(TEST_IMAGE_DIR.glob("*_similar.jpg"))

    filtered_images = set(similar.find(image_paths, hash_size=8, exclude=False))

    # Extract base names of all non-unique images
    not_unique_bases = {extract_base_name(p) for p in (similar_images | duplicate_images)}

    # Identify not_unique original images (those that have similar/duplicate counterparts)
    not_unique_originals = {p for p in image_paths if extract_base_name(p) in not_unique_bases}

    expected_included = not_unique_originals

    assert filtered_images == expected_included, (
        f"Expected {expected_included}, but got {filtered_images}"
    )
