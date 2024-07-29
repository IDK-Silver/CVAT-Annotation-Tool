from typing import Union


class Box:
    class Keys:
        label = 'box-label'
        xtl = 'box-xtl'
        ytl = 'box-ytl'
        xbr = 'box-xbr'
        ybr = 'box-ybr'
        attributes = 'box-attributes'

    @staticmethod
    def create_object() -> dict:
        obj = {
            Box.Keys.label: '',
            Box.Keys.xtl: 0.0,
            Box.Keys.ytl: 0.0,
            Box.Keys.xbr: 0.0,
            Box.Keys.ybr: 0.0,
            Box.Keys.attributes: {}
        }
        return obj

    @staticmethod
    def to_yolo_format(box: Union['Box', dict], image_width: int, image_height: int, cls_id=None,
                       to_str=False) -> Union[tuple, str]:
        """
        Convert box to YOLO format: (x_center, y_center, width, height)
        All values are normalized to [0, 1]
        """
        x_center = (box[Box.Keys.xtl] + box[Box.Keys.xbr]) / (2 * image_width)
        y_center = (box[Box.Keys.ytl] + box[Box.Keys.ybr]) / (2 * image_height)
        width = (box[Box.Keys.xbr] - box[Box.Keys.xtl]) / image_width
        height = (box[Box.Keys.ybr] - box[Box.Keys.ytl]) / image_height

        def convert_to_str(attrs):
            if to_str:
                result = ''
                for attr in attrs:
                    result += str(attr) + ' '
                return result
            else:
                return tuple(attrs)

        if cls_id is not None:
            return convert_to_str((cls_id, x_center, y_center, width, height))
        else:
            return convert_to_str((x_center, y_center, width, height))

    @staticmethod
    def to_coco_format(box: dict, image_id: int, category_id: int, box_id: int) -> dict:
        """
        Convert box to COCO format
        """
        width = box[Box.Keys.xbr] - box[Box.Keys.xtl]
        height = box[Box.Keys.ybr] - box[Box.Keys.ytl]
        return {
            "id": box_id,
            "image_id": image_id,
            "category_id": category_id,
            "bbox": [box[Box.Keys.xtl], box[Box.Keys.ytl], width, height],
            "area": width * height,
            "iscrowd": 0
        }

    @staticmethod
    def to_pascal_voc_format(box: dict) -> tuple:
        """
        Convert box to Pascal VOC format: (xmin, ymin, xmax, ymax)
        """
        return box[Box.Keys.xtl], box[Box.Keys.ytl], box[Box.Keys.xbr], box[Box.Keys.ybr]
