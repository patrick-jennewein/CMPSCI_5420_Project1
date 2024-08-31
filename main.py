import cv2
import sys
import argparse
import os
import stat
import datetime

def format_timestamp(timestamp: float) -> str:
    """convert numeric timestamp to a human-readable date and time format."""
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def print_readable_meta(meta_data_temp: os.stat_result, image: cv2.Mat, image_path: str) -> None:
    """print human-readable metadata from image."""

    print(f"\n\nDisplaying new image: ")
    # print from file path
    print(f"\t{'File Path':<20}{image_path}")
    print(f"\t{'File Type':<20}{image_path.split('.')[-1]}")

    # print from os.stat_result
    print(f"\t{'Mode':<40}{meta_data_temp.st_mode}")
    print(f"\t{'Inode':<40}{meta_data_temp.st_ino}")
    print(f"\t{'Device':<40}{meta_data_temp.st_dev}")
    print(f"\t{'Links':<40}{meta_data_temp.st_nlink}")
    print(f"\t{'User ID':<40}{meta_data_temp.st_uid}")
    print(f"\t{'Group ID':<40}{meta_data_temp.st_gid}")
    print(f"\t{'Size':<40}{meta_data_temp.st_size:,} bytes")
    print(f"\t{'Size':<40}{round(meta_data_temp.st_size / (1024 * 1024), 3)} MB")
    print(f"\t{'Access Time':<40}{format_timestamp(meta_data_temp.st_atime)}")
    print(f"\t{'Mod Time':<40}{format_timestamp(meta_data_temp.st_mtime)}")
    print(f"\t{'Create Time':<40}{format_timestamp(meta_data_temp.st_ctime)}")

    # print from image
    print(f"\t{'Width':<40}{image.shape[1]}")
    print(f"\t{'Height':<40}{image.shape[0]}")
    print(f"\t{'Extension':<40}{image_path.split('.')[-1]}")
    print("-" * 80)

def resize_image(image: cv2.Mat, max_rows: int, max_cols: int) -> cv2.Mat:
    """resize the image while maintaining aspect ratio."""
    # get current image information
    height, width = image.shape[:2]
    aspect_ratio = width / height

    # check if image actually needs resizing
    if width > max_cols or height > max_rows:
        if width > height:
            new_width = max_cols
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = max_rows
            new_width = int(new_height * aspect_ratio)

        # ensure new dimensions do not exceed maximum allowed
        new_width = min(new_width, max_cols)
        new_height = min(new_height, max_rows)

        # resize the image with the dimensions determined above
        resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return resized_image
    return image

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

def traverse_dir(start_dir) -> list:
    """traverse a single directory using depth-first search."""
    rel_file_vector = []
    stack = [start_dir]

    # possible extensions for images
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


def display_commands():
    """display commands for a simple GUI"""
    print("Commands:")
    print(f"\t{'Display next image':<40}{'n, spacebar'}")
    print(f"\t{'Display previous image':<40}{'p'}")
    print(f"\t{'Quit':<40}{'q'}")

def handle_user_input(key, current_index, file_vector):
    """navigate through GUI or quit the program"""
    quit_program = False

    # next
    if key == ord(' ') or key == ord('n'):
        if current_index < len(file_vector) - 1:
            current_index += 1
        else:
            print("End of files reached.")

    # previous
    elif key == ord('p'):
        if current_index > 0:
            current_index -= 1
        else:
            print("This is the first image.")

    # quit
    elif key == ord('q'):
        quit_program = True

    # error
    else:
        print("Unknown command. Use 'space' or 'n' for next image, 'p' for previous image, 'q' to quit.")

    return current_index, quit_program

def main(dir_path, max_rows, max_cols, file_vector):
    try:
        if len(file_vector) == 0:
            print("No image files found in the directory.")
            return 1

        current_index = 0

        while True:
            # read the image
            image_path = file_vector[current_index]
            image = cv2.imread(image_path)
            if image is None:
                print(f"Cannot open input image {image_path}")
                continue

            # resize the image if necessary
            resized_image = resize_image(image, max_rows, max_cols)

            # print metadata
            meta_data_temp = os.lstat(image_path)
            print_readable_meta(meta_data_temp, resized_image, image_path)

            # display
            cv2.imshow("color rendering", resized_image)
            display_commands()

            # wait for user input
            key = cv2.waitKey(0) & 0xFF

            # user input
            current_index, quit_program = handle_user_input(key, current_index, file_vector)
            if quit_program:
                break

        cv2.destroyAllWindows()

    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    dir_path, max_rows, max_cols = parse()
    file_vector = traverse_dir(dir_path)
    main(dir_path, max_rows, max_cols, file_vector)
