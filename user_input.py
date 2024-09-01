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