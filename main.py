# CMP SCI 5420, Professor Bhatia
# Patrick Jennewein, September 4, 2024

import cv2
import os
from print import print_readable_meta
from instructions import display_commands
from resizing import resize_image
from dfs import traverse_dir
from parse_args import parse
from user_input import handle_user_input

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
