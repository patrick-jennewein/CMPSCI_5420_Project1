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