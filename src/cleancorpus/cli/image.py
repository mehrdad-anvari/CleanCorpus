import click
from .image_filters import filter

@click.group()
def image():
    """Commands for filtering images."""
    pass

# Register subcommands
image.add_command(filter)