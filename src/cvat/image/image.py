from .box import Box
from typing import List, Union


class Image:
    class Keys:
        id = 'image-id'
        name = 'image-name'
        width = 'image-width'
        height = 'image-height'
        boxes = 'image-boxes'

    @staticmethod
    def create_object() -> dict:
        obj = {
            Image.Keys.id: '',
            Image.Keys.name: '',
            Image.Keys.width: 0,
            Image.Keys.height: 0,
            Image.Keys.boxes: []
        }
        return obj

    @staticmethod
    def get_boxs(img: Union['Image', dict]) -> List[Union[Box, dict]]:
        return img[Image.Keys.boxes]
