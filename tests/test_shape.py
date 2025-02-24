import pytest
from PIL import Image
from cleancorpus.filters.shape import find  # Update this import based on your project structure

# Helper function to create a temporary image
def create_temp_image(width, height, filename):
    img = Image.new("RGB", (width, height), color="white")
    img.save(filename)

# Fixture to create temporary images for testing
@pytest.fixture
def setup_images(tmpdir):
    # Create temporary images with different sizes and aspect ratios
    image_paths = []
    sizes = [(100, 100), (200, 200), (300, 150), (400, 400), (500, 1000)]
    for i, (width, height) in enumerate(sizes):
        filename = tmpdir.join(f"image_{i}.png")
        create_temp_image(width, height, str(filename))
        image_paths.append(str(filename))
    return image_paths

# Test cases
def test_min_width(setup_images):
    image_paths = setup_images
    filtered = find(image_paths, min_width=200, exclude=False)
    assert len(filtered) == 4  # Images with width >= 200: [200x200, 300x150, 400x400, 500x1000]

def test_max_width(setup_images):
    image_paths = setup_images
    filtered = find(image_paths, max_width=300, exclude=False)
    assert len(filtered) == 3  # Images with width <= 300: [100x100, 200x200, 300x150]

def test_min_height(setup_images):
    image_paths = setup_images
    filtered = find(image_paths, min_height=200, exclude=False)
    assert len(filtered) == 3  # Images with height >= 200: [200x200, 400x400, 500x1000]

def test_max_height(setup_images):
    image_paths = setup_images
    filtered = find(image_paths, max_height=400, exclude=False)
    assert len(filtered) == 4  # Images with height <= 400: [100x100, 200x200, 300x150, 400x400]

def test_min_aspect_ratio(setup_images):
    image_paths = setup_images
    filtered = find(image_paths, min_aspect_ratio=1.0, exclude=False)
    print(filtered)
    assert len(filtered) == 4  # Images with aspect ratio >= 1.0: [100x100, 200x200, 300x150]

def test_max_aspect_ratio(setup_images):
    image_paths = setup_images
    filtered = find(image_paths, max_aspect_ratio=1.0, exclude=False)
    assert len(filtered) == 4  # Images with aspect ratio <= 1.0: [100x100, 200x200]

def test_exclude(setup_images):
    image_paths = setup_images
    filtered = find(image_paths, min_width=200, exclude=True)
    assert len(filtered) == 1  # Images with width < 200: [100x100]

def test_invalid_image(setup_images, tmpdir):
    # Add an invalid image to the list
    invalid_image = tmpdir.join("invalid_image.txt")
    invalid_image.write("This is not an image.")
    image_paths = setup_images + [str(invalid_image)]

    filtered = find(image_paths, min_width=200, exclude=False)
    assert len(filtered) == 4  # Invalid image should be skipped