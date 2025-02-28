import importlib
import click
from .. import utils

def apply_filter(image_paths, filter_name, **kwargs):
    """Apply a filter programmatically."""
    try:
        filter_module = importlib.import_module(f"cleancorpus.filters.{filter_name}")
    except ModuleNotFoundError:
        raise click.ClickException(f"Unknown filter: {filter_name}")

    return filter_module.find(image_paths, **kwargs)

@click.group()
def filter():
    """Apply various image filters."""
    pass

@filter.command()
@click.option('--hash-size', type=int, default=8, help="Hash size for perceptual hashing.")
@click.option('--include', type=bool, default=False, help="include redundant images.")
def redundant(hash_size, include):
    """Filter similar images using perceptual hashing, keeping only one of them."""
    image_paths = utils.read_input()
    filtered_images = apply_filter(image_paths, "redundant", hash_size=hash_size, include=include)
    for path in filtered_images:
        click.echo(path)

@filter.command()
@click.option('--hash-size', type=int, default=8, help="Hash size for perceptual hashing.")
@click.option('--include', type=bool, default=False, help="include similar images.")
def similar(hash_size, include):
    """Filter similar images using perceptual hashing, keeping only one of them."""
    image_paths = utils.read_input()
    filtered_images = apply_filter(image_paths, "similar", hash_size=hash_size, include=include)
    for path in filtered_images:
        click.echo(path)


@filter.command()
@click.option('--width-range', type=(int, int), help="Min and max allowed image width.")
@click.option('--height-range', type=(int, int), help="Min and max allowed image height.")
@click.option('--aspect-ratio', type=(float, float), help="Min and max aspect ratio (width/height).")
def shape(width_range, height_range, aspect_ratio):
    """Filter images based on shape properties."""
    image_paths = utils.read_input()
    filtered_images = apply_filter(
        image_paths, "shape",
        min_width=width_range[0] if width_range else None,
        max_width=width_range[1] if width_range else None,
        min_height=height_range[0] if height_range else None,
        max_height=height_range[1] if height_range else None,
        min_aspect_ratio=aspect_ratio[0] if aspect_ratio else None,
        max_aspect_ratio=aspect_ratio[1] if aspect_ratio else None
    )
    for path in filtered_images:
        print(path)
