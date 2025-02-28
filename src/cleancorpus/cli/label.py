import click
from .. import utils

@click.group()
def label():
    """Commands for processing labels (e.g., mapping, filtering)."""
    pass

@label.command()
@click.option('--mapping-file', type=click.Path(exists=True), required=True, help="JSON file defining label mapping.")
def map(mapping_file):
    """Map labels to new classes using a mapping file."""
    label_paths = utils.read_input()
    mapped_labels = utils.map_labels(label_paths, mapping_file)
    for label in mapped_labels:
        print(label)

@label.command()
@click.option('--exclude', multiple=True, help="Labels to remove.")
def remove(remove):
    """Remove specific labels from annotations."""
    label_paths = utils.read_input()
    cleaned_labels = utils.remove_labels(label_paths, remove)
    for label in cleaned_labels:
        print(label)
