import argparse
def parse() -> tuple:
    """parse command-line arguments or use default arguments if none are given."""
    parser = argparse.ArgumentParser()

    # create optional arguments
    parser.add_argument("-rows", type=int, default=720,
                        help="Maximum number of rows in the display window [default: 720]")
    parser.add_argument("-cols", type=int, default=1080,
                        help="Maximum number of columns in the display window [default: 1080]")

    # create necessary argument
    parser.add_argument("dir", help="Directory to browse")

    # use the parsed arguments
    args = parser.parse_args()
    print(f"Browsing directory: {args.dir}")
    print(f"Rows: {args.rows}")
    print(f"Columns: {args.cols}")

    return args.dir, args.rows, args.cols
