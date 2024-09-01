import cv2
import numpy as np

def resize_image(image: cv2.Mat, max_rows: int, max_cols: int) -> cv2.Mat:
    """resize the image while maintaining aspect ratio"""
    # get current image dimensions (height and width) via numPy
    height, width = image.shape[:2]

    # determine scaling factors for width and height to fit within maxrows, maxcols
    row_scale = max_rows / height
    col_scale = max_cols / width

    # choose the smaller scaling factor to (1) maintain aspect ratio and (2) ensure it fits in user-defined parameters
    scale_factor = min(row_scale, col_scale)

    # compute the new dimensions
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    # define the transformation matrix (identity scaled by the scale factor)
    transformation_matrix = np.float32([[scale_factor, 0, 0],       # scales the width
                                        [0, scale_factor, 0]])      # scales the height

    # apply the affine transformation
    resized_image = cv2.warpAffine(image, transformation_matrix, (new_width, new_height))

    return resized_image
