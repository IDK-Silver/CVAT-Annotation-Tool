import numpy as np
from PIL import Image
import cv2
from typing import Union

import numpy as np
import cv2
from typing import Union

def segment_image_with_mask(image: Union[np.ndarray, str], mask: np.ndarray, top: int = 0, left: int = 0, is_crop: bool = False) -> np.ndarray:
    """
    Segment a color image using a 2D binary mask with given offsets.

    Parameters:
    image (Union[np.ndarray, str]): Input color image as NumPy array (OpenCV format) or file path
    mask (np.ndarray): 2D binary mask
    top (int): Vertical offset of the mask relative to the image top
    left (int): Horizontal offset of the mask relative to the image left
    is_crop (bool): Whether to crop the result to the mask boundaries

    Returns:
    np.ndarray: Segmented image (OpenCV format)
    """
    # Read or convert the original image
    if isinstance(image, str):
        original_image = cv2.imread(image, cv2.IMREAD_UNCHANGED)
    elif isinstance(image, np.ndarray):
        original_image = image.copy()
    else:
        raise ValueError("Unsupported image format")
    
    # Ensure the mask is binary
    binary_mask = mask.astype(bool)
    
    # Create a transparent layer of the same size as the original image
    if original_image.shape[2] == 3:
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2BGRA)
        result = np.zeros((original_image.shape[0], original_image.shape[1], 4), dtype=np.uint8)
        result[:,:,3] = 0  # Set alpha channel to fully transparent
    else:
        result = np.zeros_like(original_image)
    
    # Get dimensions of the image and mask
    img_height, img_width = original_image.shape[:2]
    mask_height, mask_width = binary_mask.shape
    
    # Calculate valid mask area
    valid_top = max(0, top)
    valid_left = max(0, left)
    valid_bottom = min(img_height, top + mask_height)
    valid_right = min(img_width, left + mask_width)
    
    # Apply mask to the valid area
    for y in range(valid_top, valid_bottom):
        for x in range(valid_left, valid_right):
            mask_y = y - top
            mask_x = x - left
            if 0 <= mask_y < mask_height and 0 <= mask_x < mask_width:
                if binary_mask[mask_y, mask_x]:
                    result[y, x] = original_image[y, x]
    
    # Crop the result image if is_crop is True
    if is_crop:
        # Find the boundaries of non-zero elements in the mask
        rows = np.any(binary_mask, axis=1)
        cols = np.any(binary_mask, axis=0)
        ymin, ymax = np.where(rows)[0][[0, -1]]
        xmin, xmax = np.where(cols)[0][[0, -1]]
        
        # Calculate the crop area
        crop_top = max(0, top + ymin)
        crop_left = max(0, left + xmin)
        crop_bottom = min(img_height, top + ymax + 1)
        crop_right = min(img_width, left + xmax + 1)
        
        # Crop the result image
        result = result[crop_top:crop_bottom, crop_left:crop_right]
    
    return result

def overlay_image(background, overlay, top, left):
    """
    Overlay one image on top of another.

    Parameters:
    background (np.ndarray): Background image in OpenCV format
    overlay (np.ndarray): Image to be overlaid in OpenCV format
    top (int): Y-coordinate of the top-left corner of the overlay image
    left (int): X-coordinate of the top-left corner of the overlay image

    Returns:
    np.ndarray: Resulting image after overlay in OpenCV format
    """
    
    x = int(left)
    y = int(top)
    
    # Get dimensions of background and overlay images
    h, w = overlay.shape[:2]
    bg_h, bg_w = background.shape[:2]

    # Calculate valid overlay area
    x1, x2 = max(x, 0), min(x + w, bg_w)
    y1, y2 = max(y, 0), min(y + h, bg_h)

    # Calculate valid area of the overlay image
    overlay_x1 = max(0, -x)
    overlay_y1 = max(0, -y)
    overlay_x2 = min(w, bg_w - x)
    overlay_y2 = min(h, bg_h - y)

    # Check if there's an overlapping area
    if x1 >= x2 or y1 >= y2 or overlay_x1 >= overlay_x2 or overlay_y1 >= overlay_y2:
        return background

    # Create mask for the overlay area
    if overlay.shape[2] == 4:
        # If overlay image has an alpha channel
        alpha = overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2, 3] / 255.0
        alpha = np.expand_dims(alpha, axis=-1)
        overlay_colors = overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2, :3]
    else:
        # If overlay image doesn't have an alpha channel, assume fully opaque
        alpha = np.ones((y2-y1, x2-x1, 1))
        overlay_colors = overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2]

    # Perform image overlay
    background[y1:y2, x1:x2] = (1 - alpha) * background[y1:y2, x1:x2] + alpha * overlay_colors

    return background