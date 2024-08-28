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
    """
        Traverse a directory and return a list of all files and directories.

        This function performs a DFS from 'start_dir' and iterates through the current
        directory path ('root'), the list of subdirectories ('dirs') and the list
        of files in the current directory ('files'). As the function
        iterates, metadata is found, and file path names are created and added to the vector.
    """

    file_vector = []                                # vector to store file paths
    meta_data_vector = []                                  # vector to store meta_data

    # depth-first search through directories
    for root, dirs, files in os.walk(start_dir):
        # create file paths by iterating through files + directories at that level
        for name in files + dirs:
            full_path = os.path.join(root, name)
            relative_path = os.path.relpath(full_path, start_dir)
            print(full_path)
            print(relative_path)
            try:
                # get file metadata
                meta_data = os.lstat(full_path)
                meta_data_vector.append(meta_data)


                # check if directory
                if stat.S_ISDIR(meta_data.st_mode):
                    file_vector.append(f'Directory: {relative_path}')

                # check if file
                else:
                    file_vector.append(relative_path)
            except OSError as e:
                print(f"Error accessing {full_path}: {e}")

    return file_vector, meta_data_vector


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
    file_vector, meta_data_vector = traverse_dir(starting_directory)
    for file, meta in zip(file_vector, meta_data_vector):
        print(f"filename: {file}")
        print(f"{'\tst_size: ':<40}{meta[6]} bytes")
        print(f"{'\tst_atime (access time): ':<40}{format_timestamp(meta[7])}")
        print(f"{'\tst_mtime (modification time): ':<40}{format_timestamp(meta[8])}")
        print(f"{'\tst_ctime (status change time): ':<40}{format_timestamp(meta[9])}")
    main(args, file_vector, meta_data_vector)

