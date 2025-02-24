import sys
import argparse
import importlib
from . import utils

def apply_filter(image_paths, action, filter_name, **kwargs):
    """Apply a filter programmatically."""
    try:
        filter_module = importlib.import_module(f".filters.{filter_name}", package="cleancorpus")
    except ModuleNotFoundError:
        raise ValueError(f"Unknown filter: {filter_name}")

    return filter_module.find(image_paths, exclude=(action == "exclude"), **kwargs)

def cli():
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="cleancorpus - Clean and preprocess datasets using UNIX pipes.")
    
    parser.add_argument("action", choices=["include", "exclude"], help="Include or exclude specific images")
    parser.add_argument("filter", help="Filter type (e.g., 'similar', 'redundant', 'shape')")

    similar_group = parser.add_argument_group("similar/redundant filter options")
    similar_group.add_argument("--hash_size", type=int, default=8, help="Hash size for duplicate detection (only for 'similar' filter)")

     # shape filter args
    shape_group = parser.add_argument_group("shape filter options")
    shape_group.add_argument("--min_width", type=int, help="Minimum allowed image width")
    shape_group.add_argument("--min_height", type=int, help="Minimum allowed image height")
    shape_group.add_argument("--max_width", type=int, help="Maximum allowed image width")
    shape_group.add_argument("--max_height", type=int, help="Maximum allowed image height")
    shape_group.add_argument("--min_aspect_ratio", type=float, help="Minimum allowed aspect ratio (width/height)")
    shape_group.add_argument("--max_aspect_ratio", type=float, help="Maximum allowed aspect ratio (width/height)")

    args = parser.parse_args()

    # Read input files (from stdin or command line)
    image_paths = utils.read_input()

    match args.filter:
        case "similar":
            filtered_images = apply_filter(image_paths, args.action, args.filter, hash_size=args.hash_size)
        case "redundant":
            filtered_images = apply_filter(image_paths, args.action, args.filter, hash_size=args.hash_size)
        case "shape":
            filtered_images = apply_filter(
                image_paths,
                args.action,
                args.filter,
                min_width=args.min_width,
                min_height=args.min_height,
                max_width=args.max_width,
                max_height=args.max_height,
                min_aspect_ratio=args.min_aspect_ratio,
                max_aspect_ratio=args.max_aspect_ratio
            )
        case _ :
            print(f"Filter {args.filter} is NOT implemented!", file=sys.stderr)

    for path in filtered_images:
        print(path)

if __name__ == "__main__":
    cli()
