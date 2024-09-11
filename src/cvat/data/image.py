from .box import Box
from typing import List, Union
from .mask import Mask

class Image:
    class Keys:
        id = 'image-id'
        name = 'image-name'
        width = 'image-width'
        height = 'image-height'
        boxes = 'image-boxes'
        masks = 'image-masks'

    @staticmethod
    def create_object() -> dict:
        obj = {
            Image.Keys.id: '',
            Image.Keys.name: '',
            Image.Keys.width: 0,
            Image.Keys.height: 0,
            Image.Keys.boxes: [],
            Image.Keys.masks: []
        }
        return obj

    @staticmethod
    def get_boxs(img: Union['Image', dict]) -> List[Union[Box, dict]]:
        return img[Image.Keys.boxes]
    
    @staticmethod
    def get_masks(img: Union['Image', dict]) -> List[Union[Mask, dict]]:
        return img[Image.Keys.masks]
