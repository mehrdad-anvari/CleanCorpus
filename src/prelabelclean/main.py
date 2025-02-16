import sys
import argparse
import importlib
from . import utils

def apply_filter(image_paths, action, filter_name, **kwargs):
    """Apply a filter programmatically."""
    try:
        filter_module = importlib.import_module(f".filters.{filter_name}", package="prelabelclean")
    except ModuleNotFoundError:
        raise ValueError(f"Unknown filter: {filter_name}")

    return filter_module.find(image_paths, exclude=(action == "exclude"), **kwargs)

def cli():
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="PreLabelClean - Clean and preprocess datasets using UNIX pipes.")
    
    parser.add_argument("action", choices=["include", "exclude"], help="Include or exclude specific images")
    parser.add_argument("filter", help="Filter type (e.g., 'similar', 'redundant')")
    parser.add_argument("--threshold", type=int, default=0, help="Threshold for mostly gray images (only for 'gray' filter)")
    parser.add_argument("--hash_size", type=int, default=8, help="Hash size for duplicate detection (only for 'similar' filter)")

    args = parser.parse_args()

    # Read input files (from stdin or command line)
    image_paths = utils.read_input()

    match args.filter:
        case "similar":
            filtered_images = apply_filter(image_paths, args.action, args.filter, hash_size=args.hash_size)
        case "redundant":
            filtered_images = apply_filter(image_paths, args.action, args.filter, hash_size=args.hash_size)
        case _ :
            print(f"Filter {args.filter} is NOT implemented!", file=sys.stderr)

    for path in filtered_images:
        print(path)

if __name__ == "__main__":
    cli()
