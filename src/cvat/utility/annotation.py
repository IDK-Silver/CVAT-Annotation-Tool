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

def rle_to_yolo_rectangle(
    rle_height: int, rle_width: int,
    rle_top: int, rle_left: int,
    image_height: int, image_width: int
    ) -> np.ndarray:
    
    # 計算矩形中心點的 x 和 y 座標
    center_x = rle_left + rle_width / 2
    center_y = rle_top + rle_height / 2
    
    # 將座標轉換為相對於圖像大小的比例
    x = center_x / image_width
    y = center_y / image_height
    
    # 計算寬度和高度的比例
    w = rle_width / image_width
    h = rle_height / image_height
    
    # 返回 YOLO 格式的矩形 [x, y, w, h]
    return np.array([x, y, w, h], dtype=np.float32)


def rle_to_voc_rectangle(
        rle_height: int, rle_width: int,
        rle_top: int, rle_left: int,
        image_height: int, image_width: int
    ) -> np.ndarray:
    # 計算矩形的左上角和右下角坐標
    xmin = rle_left
    ymin = rle_top
    xmax = rle_left + rle_width
    ymax = rle_top + rle_height

    # 確保坐標不超出圖像邊界
    xmin = max(0, xmin)
    ymin = max(0, ymin)
    xmax = min(image_width, xmax)
    ymax = min(image_height, ymax)

    # 返回 VOC 格式的矩形 [xmin, ymin, xmax, ymax]
    return np.array([xmin, ymin, xmax, ymax], dtype=np.int32)