import zlib
import sys


def split_dataset(items: list, split_ratio: float):
    # Check if the split ratio is within the valid range
    if not 0 <= split_ratio <= 1:
        print(f"Error: split_ratio must be between 0 and 1. Got {split_ratio}")
        sys.exit(1)

    # Initialize lists to store the split data
    primary_set = []
    secondary_set = []

    # Iterate through all items in the dataset
    for item in items:
        # Calculate CRC32 for the current item
        if isinstance(item, str):
            item_crc = zlib.crc32(item.encode())
        else:
            item_crc = zlib.crc32(str(item).encode())

        # Determine which set to put the item in based on its CRC32 value
        if (item_crc & 0xFFFFFFFF) / 0xFFFFFFFF < split_ratio:
            primary_set.append(item)
        else:
            secondary_set.append(item)

    return primary_set, secondary_set
