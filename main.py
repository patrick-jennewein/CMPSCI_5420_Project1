import cv2
import sys
import random
import time
import argparse             # for parsing the command line
import os                   # for finding file path
import stat                 # for file metadata
import datetime             # for formatting metadata

def format_timestamp(timestamp):
    """Convert timestamp to a human-readable date and time format."""
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def parse() -> tuple:
    """ Parse command-line arguments."""
    parser = argparse.ArgumentParser()

    # create arguments
    parser.add_argument("-rows", type=int, default=720,
                        help="Maximum number of rows in the display window [default: 720]")
    parser.add_argument("-cols", type=int, default=1080,
                        help="Maximum number of columns in the display window [default: 1080]")
    parser.add_argument("dir", help="Directory to browse")

    # Parse arguments
    args = parser.parse_args()

    # Use the parsed arguments
    print(f"Browsing directory: {args.dir}")
    print(f"Rows: {args.rows}")
    print(f"Columns: {args.cols}")

    return args.dir, args.rows, args.cols

def traverse_dir(start_dir) -> list:
    file_vector = []
    meta_vector = []
    stack = [start_dir]
    image_extensions = {".jpeg", ".jpg", ".png", ".gif", ".bmp", ".tiff", ".webp"}

    # keep iterating through stack until empty
    while stack:
        current_path = stack.pop()

        try:
            # get metadata to see if file or directory
            meta_data_temp = os.lstat(current_path)

            # If directory, explore directory for DFS
            if stat.S_ISDIR(meta_data_temp.st_mode):
                with os.scandir(current_path) as entries:
                    for entry in reversed(list(entries)):
                        stack.append(entry.path)

            # If it's a file, add it to the file_vector
            else:
                # Check if the file extension matches any in our image_extensions set
                _, file_extension = os.path.splitext(current_path)
                if file_extension.lower() in image_extensions:
                    relative_path = os.path.relpath(current_path, start_dir)
                    file_vector.append(relative_path)
                    meta_vector.append(meta_data_temp.st_size)


        except OSError as e:
            print(f"Error accessing {current_path}: {e}")

    print(file_vector)
    print(meta_vector)
    return file_vector


def main(args, file_vector, meta_data_vector):
    try:
        if len(sys.argv) != 2:
            print(f"usage: {sys.argv[0]} image_file")
            return 1

        # Read the image
        image = cv2.imread(file_vector[6])

        # Make sure that the image is read properly
        if image is None:
            raise Exception(f"Cannot open input image {sys.argv[1]}")

        # Image dimensions
        print(f"Image size is: {image.shape[1]}x{image.shape[0]}")  # width x height

        # Read the same image as a grayscale image
        img_gray = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)

        # Display color image
        cv2.imshow("Color Rendering", image)
        cv2.waitKey(0)

        # Display grayscale image
        cv2.imshow("Grayscale Rendering", img_gray)
        cv2.waitKey(0)

        # Save a copy of grayscale image to disk
        gray_pic_file = sys.argv[1].rsplit('.', 1)
        gray_pic_file = f"{gray_pic_file[0]}_gray.{gray_pic_file[1]}"
        cv2.imwrite(gray_pic_file, img_gray)

        # Display value at a random pixel
        random.seed(time.time())
        r = random.randint(0, image.shape[0] - 1)
        c = random.randint(0, image.shape[1] - 1)

        pxl_color = image[r, c]
        print(f"Color pixel at ({r},{c}) = ({int(pxl_color[0])}, {int(pxl_color[1])}, {int(pxl_color[2])})")

        pxl_gray = img_gray[r, c]
        print(f"Gray scale pixel at ({r},{c}) = {int(pxl_gray)}")

    except Exception as e:
        print(f"Error: {sys.argv[0]}: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    args = parse()
    starting_directory = args[0]
    file_vector = traverse_dir(starting_directory)
    # for file, meta in zip(file_vector, meta_data_vector):
    #     print(f"filename: {file}")
    #     print(f"{'\tst_size: ':<40}{meta[6]} bytes")
    #     print(f"{'\tst_atime (access time): ':<40}{format_timestamp(meta[7])}")
    #     print(f"{'\tst_mtime (modification time): ':<40}{format_timestamp(meta[8])}")
    #     print(f"{'\tst_ctime (status change time): ':<40}{format_timestamp(meta[9])}")
    # main(args, file_vector, meta_data_vector)

