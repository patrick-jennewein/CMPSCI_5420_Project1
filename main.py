import cv2
import sys
import random
import time
import argparse             # for parsing the command line
import os                   # for finding file path
import stat                 # for file metadata
import datetime             # for formatting metadata

def format_timestamp(timestamp) -> str:
    """convert timestamp to a human-readable date and time format."""
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def print_readable_meta(file_path: str, metadata: dict) -> None:
    """print metadata for a single file in a human-readable format."""
    print(f"\nFile Path: {file_path}")
    print(f"\t{'Mode':<20}{metadata[file_path]['st_mode']}")
    print(f"\t{'Inode':<20}{metadata[file_path]['st_ino']}")
    print(f"\t{'Device':<20}{metadata[file_path]['st_dev']}")
    print(f"\t{'Links':<20}{metadata[file_path]['st_nlink']}")
    print(f"\t{'User ID':<20}{metadata[file_path]['st_uid']}")
    print(f"\t{'Group ID':<20}{metadata[file_path]['st_gid']}")
    print(f"\t{'Size':<20}{metadata[file_path]['st_size']:,} bytes")
    print(f"\t{'Size':<20}{round(metadata[file_path]['st_size'] / (1024 * 1024), 3)} MB")
    print(f"\t{'Access Time':<20}{metadata[file_path]['st_atime']}")
    print(f"\t{'Mod Time':<20}{metadata[file_path]['st_mtime']}")
    print(f"\t{'Create Time':<20}{metadata[file_path]['st_ctime']}")
    print(f"\t{'Width':<20}{metadata[file_path]['width']}")
    print(f"\t{'Height':<20}{metadata[file_path]['height']}")
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
    # set up traversal
    rel_file_vector = []
    meta_vector = {}
    stack = [start_dir]

    # provide possible extensions for images
    image_extensions = {".jpeg", ".jpg", ".png", ".gif", ".bmp", ".tiff", ".webp"}

    # keep iterating through stack until empty
    while stack:
        current_path = stack.pop()

        try:
            # get metadata to see if file or directory
            meta_data_temp = os.lstat(current_path)

            # if directory, explore directory for DFS
            if stat.S_ISDIR(meta_data_temp.st_mode):
                with os.scandir(current_path) as entries:
                    for entry in reversed(list(entries)):
                        stack.append(entry.path)

            # if it's a file, add data to the file_vector and meta_vector
            else:
                # check if the file extension matches any in image_extensions set
                _, file_extension = os.path.splitext(current_path)
                if file_extension.lower() in image_extensions:
                    relative_path = os.path.relpath(current_path, start_dir)
                    rel_file_vector.append(f"{start_dir}\\{relative_path}")

                    # create a dictionary of os.stat_result values with formatted timestamps
                    image = cv2.imread(f"{start_dir}\\{relative_path}")
                    meta_vector[f"{start_dir}\\{relative_path}"] = {
                        "st_mode": meta_data_temp.st_mode,
                        "st_ino": meta_data_temp.st_ino,
                        "st_dev": meta_data_temp.st_dev,
                        "st_nlink": meta_data_temp.st_nlink,
                        "st_uid": meta_data_temp.st_uid,
                        "st_gid": meta_data_temp.st_gid,
                        "st_size": meta_data_temp.st_size,
                        "st_atime": format_timestamp(meta_data_temp.st_atime),
                        "st_mtime": format_timestamp(meta_data_temp.st_mtime),
                        "st_ctime": format_timestamp(meta_data_temp.st_ctime),
                        "width": image.shape[1],
                        "height": image.shape[0]
                    }

        except OSError as e:
            print(f"Error accessing {current_path}: {e}")

    return rel_file_vector, meta_vector


def main(args, file_vector, meta_data_vector):
    try:
        if len(sys.argv) != 2:
            print(f"usage: {sys.argv[0]} image_file")
            return 1

        # Read the image and print metadata
        image = cv2.imread(file_vector[0])
        print_readable_meta(file_vector[0], meta_data_vector)

        # Make sure that the image is read properly
        if image is None:
            raise Exception(f"Cannot open input image {sys.argv[1]}")

        # Display color image
        cv2.imshow("Color Rendering", image)
        cv2.waitKey(0)

    except Exception as e:
        print(f"Error: {sys.argv[0]}: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    args = parse()
    starting_directory = args[0]
    file_vector, meta_vector = traverse_dir(starting_directory)
    main(args, file_vector, meta_vector)

