import cv2
import sys
import random
import time
import argparse             # for parsing the command line
import os
import stat

def parse():
    """
        Parse command-line arguments.
    """
    parser = argparse.ArgumentParser()

    # create arguments
    parser.add_argument("-rows", type=int, default=720, help="Maximum number of rows in the display window [default: 720]")
    parser.add_argument("-cols", type=int, default=1080, help="Maximum number of columns in the display window [default: 1080]")
    parser.add_argument("dir", help="Directory to browse")

    # Parse arguments
    args = parser.parse_args()

    # Use the parsed arguments
    print(f"Browsing directory: {args.dir}")
    print(f"Rows: {args.rows}")
    print(f"Columns: {args.cols}")

    return (args.dir, args.rows, args.cols)

def traverse_dir(start_dir):
    """
        Traverse a directory and return a list of all files and directories.
    """
    file_vector = []

    # Conduct a depth-first search through directories
    for root, dirs, files in os.walk(start_dir):
        for name in files + dirs:
            full_path = os.path.join(root, name)
            relative_path = os.path.relpath(full_path, start_dir)
            print(full_path)
            print(relative_path)
            try:
                # Using lstat to get file metadata
                file_stat = os.lstat(full_path)

                # Check if the entry is a directory using S_ISDIR
                if stat.S_ISDIR(file_stat.st_mode):
                    # Recursively handle directory traversal (DFS)
                    file_vector.append(f'Directory: {relative_path}')
                else:
                    # If it's a file, add it to the vector
                    file_vector.append(relative_path)
            except OSError as e:
                print(f"Error accessing {full_path}: {e}")
    return file_vector


def main(args):
    print(args)
    # try:
    #     if len(sys.argv) != 2:
    #         print(f"usage: {sys.argv[0]} image_file")
    #         return 1
    #
    #     # Read the image
    #     image = cv2.imread(sys.argv[1])
    #
    #     # Make sure that the image is read properly
    #     if image is None:
    #         raise Exception(f"Cannot open input image {sys.argv[1]}")
    #
    #     # Image dimensions
    #     print(f"Image size is: {image.shape[1]}x{image.shape[0]}")  # width x height
    #
    #     # Read the same image as a grayscale image
    #     img_gray = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    #
    #     # Display color image
    #     cv2.imshow("Color Rendering", image)
    #     cv2.waitKey(0)
    #
    #     # Display grayscale image
    #     cv2.imshow("Grayscale Rendering", img_gray)
    #     cv2.waitKey(0)
    #
    #     # Save a copy of grayscale image to disk
    #     gray_pic_file = sys.argv[1].rsplit('.', 1)
    #     gray_pic_file = f"{gray_pic_file[0]}_gray.{gray_pic_file[1]}"
    #     cv2.imwrite(gray_pic_file, img_gray)
    #
    #     # Display value at a random pixel
    #     random.seed(time.time())
    #     r = random.randint(0, image.shape[0] - 1)
    #     c = random.randint(0, image.shape[1] - 1)
    #
    #     pxl_color = image[r, c]
    #     print(f"Color pixel at ({r},{c}) = ({int(pxl_color[0])}, {int(pxl_color[1])}, {int(pxl_color[2])})")
    #
    #     pxl_gray = img_gray[r, c]
    #     print(f"Gray scale pixel at ({r},{c}) = {int(pxl_gray)}")
    #
    # except Exception as e:
    #     print(f"Error: {sys.argv[0]}: {str(e)}")
    #     return 1
    #
    # return 0


if __name__ == "__main__":
    args = parse()
    starting_directory = args[0]
    vector = traverse_dir(starting_directory)
    main(args)

