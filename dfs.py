import stat
import os
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