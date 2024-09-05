import datetime
import os
def format_timestamp(timestamp: float) -> str:
    """convert numeric timestamp to a human-readable date and time format."""
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def print_readable_meta(meta_data_temp: os.stat_result, image, image_path: str, current_index:int) -> None:
    """print human-readable metadata from image."""
    # print from file path
    filename = os.path.splitext(os.path.basename(image_path))[0]
    size = round(meta_data_temp.st_size / (1024 * 1024), 3)
    path = image_path
    width = image.shape[0]
    height = image.shape[1]
    print(f"{current_index:>5}{size:>10} MB  {width} x {height}     {path:>70}")
