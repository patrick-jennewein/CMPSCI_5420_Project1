def handle_user_input(key, current_index, file_vector):
    """navigate through GUI or quit the program"""
    quit_program = False

    # next
    if key == ord(' ') or key == ord('n'):
        if current_index < len(file_vector) - 1:
            current_index += 1

    # previous
    elif key == ord('p'):
        if current_index > 0:
            current_index -= 1

    # quit
    elif key == ord('q'):
        quit_program = True

    return current_index, quit_program