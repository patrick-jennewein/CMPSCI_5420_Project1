import datetime
import os
def format_timestamp(timestamp: float) -> str:
    """convert numeric timestamp to a human-readable date and time format."""
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def print_readable_meta(meta_data_temp: os.stat_result, image, image_path: str) -> None:
    """print human-readable metadata from image."""
    print(f"\n\nDisplaying new image: ")
    # print from file path
    filename = os.path.splitext(os.path.basename(image_path))[0]
    print(f"\t{'File Name':<40}{filename}")
    print(f"\t{'File Path':<40}{image_path}")
    print(f"\t{'File Type':<40}{image_path.split('.')[-1]}")

    # print from os.stat_result
    print(f"\t{'Mode':<40}{meta_data_temp.st_mode}")
    print(f"\t{'Inode':<40}{meta_data_temp.st_ino}")
    print(f"\t{'Device':<40}{meta_data_temp.st_dev}")
    print(f"\t{'Links':<40}{meta_data_temp.st_nlink}")
    print(f"\t{'User ID':<40}{meta_data_temp.st_uid}")
    print(f"\t{'Group ID':<40}{meta_data_temp.st_gid}")
    print(f"\t{'Access Time':<40}{format_timestamp(meta_data_temp.st_atime)}")
    print(f"\t{'Mod Time':<40}{format_timestamp(meta_data_temp.st_mtime)}")
    print(f"\t{'Create Time':<40}{format_timestamp(meta_data_temp.st_ctime)}")
    print(f"\t{'Size (Bytes)':<40}{meta_data_temp.st_size:,} bytes")
    print(f"\t{'Size (MB)':<40}{round(meta_data_temp.st_size / (1024 * 1024), 3)} MB")

    # print from image
    print(f"\t{'Size (Width)':<40}{image.shape[1]}")
    print(f"\t{'Size (Height)':<40}{image.shape[0]}")
    print(f"\t{'Pixels':<40}{(image.shape[0] * image.shape[1]):,}")
    print(f"\t{'Extension':<40}{image_path.split('.')[-1]}")
    print("-" * 80)

def display_commands():
    """display commands for a simple GUI"""
    print("Commands:")
    print(f"\t{'Display next image':<40}{'n, spacebar'}")
    print(f"\t{'Display previous image':<40}{'p'}")
    print(f"\t{'Quit':<40}{'q'}")