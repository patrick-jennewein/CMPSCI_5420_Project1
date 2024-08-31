import cv2
import sys
import random
import time
import argparse             # for parsing the command line
import os                   # for finding file path
import stat                 # for file metadata
import datetime             # for formatting metadata

def format_timestamp(timestamp: float) -> str:
    """convert numeric timestamp to a human-readable date and time format."""
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def print_readable_meta(meta_data_temp: os.lstat, image: cv2.imread, image_path: str) -> None:
    """print human-readable metadata from image"""
    print(f"\t{'File Path':<20}{image_path}")
    print(f"\t{'File Type':<20}{image_path.split('.')[-1]}")
    print(f"\t{'Mode':<20}{meta_data_temp.st_mode}")
    print(f"\t{'Inode':<20}{meta_data_temp.st_ino}")
    print(f"\t{'Device':<20}{meta_data_temp.st_dev}")
    print(f"\t{'Links':<20}{meta_data_temp.st_nlink}")
    print(f"\t{'User ID':<20}{meta_data_temp.st_uid}")
    print(f"\t{'Group ID':<20}{meta_data_temp.st_gid}")
    print(f"\t{'Size':<20}{meta_data_temp.st_size:,} bytes")
    print(f"\t{'Size':<20}{round(meta_data_temp.st_size / (1024 * 1024), 3)} MB")
    print(f"\t{'Access Time':<20}{meta_data_temp.st_atime}")
    print(f"\t{'Mod Time':<20}{meta_data_temp.st_mtime}")
    print(f"\t{'Create Time':<20}{meta_data_temp.st_ctime}")
    print(f"\t{'Width':<20}{image.shape[1]}")
    print(f"\t{'Height':<20}{image.shape[0]}")
    print(f"\t{'Extension':<20}{image.shape[0]}")
    print("-" * 40)


def parse() -> tuple:
    """ parse command-line arguments or use default arguments if none are given"""
    parser = argparse.ArgumentParser()

    # create optional arguments
    parser.add_argument("-rows", type = int, default = 720,
                        help="Maximum number of rows in the display window [default: 720]")
    parser.add_argument("-cols", type = int, default = 1080,
                        help="Maximum number of columns in the display window [default: 1080]")

    # create necessary argument
    parser.add_argument("dir", help = "Directory to browse")

    # use the parsed arguments
    args = parser.parse_args()
    print(f"Browsing directory: {args.dir}")
    print(f"Rows: {args.rows}")
    print(f"Columns: {args.cols}")

    return args.dir, args.rows, args.cols


def traverse_dir(start_dir) -> tuple:
    """traverse a single directory using depth-first search"""
    rel_file_vector = []
    stack = [start_dir]

    # provide possible extensions for images
    image_extensions = {".jpeg", ".jpg", ".png", ".gif", ".bmp", ".tiff", ".webp"}

    # keep iterating through stack until empty
    while stack:
        current_path = stack.pop()

        try:
            # get metadata to see if file or directory
            meta_data_temp = os.lstat(current_path)

            # if directory, 'explore' directory for DFS
            if stat.S_ISDIR(meta_data_temp.st_mode):
                with os.scandir(current_path) as entries:
                    for entry in reversed(list(entries)):
                        stack.append(entry.path)

            # if it's a file that matches image extensions, add data to the file_vector
            else:
                _, file_extension = os.path.splitext(current_path)
                if file_extension.lower() in image_extensions:
                    relative_path = os.path.relpath(current_path, start_dir)
                    rel_file_vector.append(f"{start_dir}\\{relative_path}")

        except OSError as e:
            print(f"Error accessing {current_path}: {e}")

    return rel_file_vector


def main(args, file_vector):
    try:
        if len(sys.argv) != 2:
            print(f"usage: {sys.argv[0]} image_file")
            return 1

        # Read the image
        image_path = file_vector[0]
        image = cv2.imread(image_path)
        if image is None:
            raise Exception(f"Cannot open input image {sys.argv[1]}")

        # print metadata
        meta_data_temp = os.lstat(image_path)
        print_readable_meta(meta_data_temp, image, image_path)

        # display
        cv2.imshow("Color Rendering", image)
        cv2.waitKey(0)

    except Exception as e:
        print(f"Error: {sys.argv[0]}: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    args = parse()
    starting_directory = args[0]
    file_vector = traverse_dir(starting_directory)
    main(args, file_vector)

