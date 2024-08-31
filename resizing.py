import cv2
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
