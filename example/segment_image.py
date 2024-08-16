import cvat
import cv2
import numpy as np

# Load annotation file
file = cvat.core.CVAT()
file.load('./dataset/annotations.xml')

# Get image info from annotation file
images_info = file.get_images()

# Select first image
image_info: cvat.data.Image = None
if len(images_info) >= 1:
    image_info = images_info[0]
else:
    print('Failed to get image info, no images exist.')
    exit(-1)

# Get masks info from first image
image_masks_info = cvat.data.Image.get_masks(image_info)

# Get first mask info
image_mask_info: cvat.data.Mask = None
if len(image_masks_info) >= 1:
    image_mask_info = image_masks_info[0]
else:
    print('Failed to get mask info, no masks exist.')
    exit(-1)

# Get mask from mask info
image_mask = cvat.utility.annotation.rle_to_binary_mask(
    image_mask_info[cvat.data.Mask.Keys.rle],
    image_mask_info[cvat.data.Mask.Keys.height],
    image_mask_info[cvat.data.Mask.Keys.width]
)

black_white_mask_image  = (image_mask * 255).astype(np.uint8)

# Save as black and white image
cv2.imwrite('./result/black_white_mask_image.png', black_white_mask_image)

# Read image that mask belongs to
item_image = cv2.imread(
    './dataset/images/' + image_info[cvat.data.Image.Keys.name]
)

segment_image = cvat.utility.image.segment_image_with_mask(
    item_image, image_mask,
    image_mask_info[cvat.data.Mask.Keys.top],
    image_mask_info[cvat.data.Mask.Keys.left],
    is_crop=True
)
cv2.imwrite('./result/segment_image.jpg', segment_image)

# Read background image
background_image = cv2.imread(
    './images/background.jpg'
)

# Overlay segmented image on background
overlay_image = cvat.utility.image.overlay_image(
    background_image, segment_image,
    (background_image.shape[0] - segment_image.shape[0]) / 2,
    (background_image.shape[1] - segment_image.shape[1]) / 2
)
cv2.imwrite('./result/overlay_image.jpg', overlay_image)