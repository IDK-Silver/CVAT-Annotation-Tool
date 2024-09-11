from typing import List, Union


class Mask:
    class Keys:
        label = 'mask-label'
        source = 'mask-source'
        occluded = 'mask-occluded'
        rle = 'mask-rle'
        left = 'mask-left'
        top = 'mask-top'
        height = 'mask-height'
        width = 'mask-width'
        

    @staticmethod
    def create_object() -> dict:
        obj = {
            Mask.Keys.label: '',
            Mask.Keys.source: '',
            Mask.Keys.occluded: False,
            Mask.Keys.rle: str,
            Mask.Keys.left: 0,
            Mask.Keys.top: 0,
            Mask.Keys.height: 0,
            Mask.Keys.width: 0
        }
        return obj

    @staticmethod
    def get_data(mask: Union['Mask', dict]) -> List[int]:
        return mask[Mask.Keys.rle]
    
    


