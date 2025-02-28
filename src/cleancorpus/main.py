import click
from .cli.image import image
from .cli.label import label

@click.group()
def cli():
    """CleanCorpus - A tool for cleaning and preprocessing datasets."""
    pass

# Register subcommands
cli.add_command(image)
cli.add_command(label)

if __name__ == "__main__":
    cli()