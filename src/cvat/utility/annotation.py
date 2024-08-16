import numpy as np
from typing import Union

def rle_to_mask(rle: Union[str, list], class_id: int, height: int, width: int) -> np.ndarray:
    
    if type(rle) == str:
       rle = [int(num) for num in rle.split(', ')] if rle else []
    
    total_pixels = height * width
    mask = np.zeros(total_pixels, dtype=np.uint8)
    
    current_position = 0
    for i in range(0, len(rle), 2):
        start = current_position + rle[i]
        if i + 1 < len(rle):
            length = rle[i + 1]
            mask[start:start + length] = class_id
            current_position = start + length
        else:
            # 如果是最後一個值且沒有對應的長度，填充到圖像結束
            mask[start:] = class_id
    
    return mask.reshape(height, width)

def rle_to_binary_mask(rle: list, height: int, width: int) -> np.ndarray:
    return rle_to_mask(rle, 1, height, width)

