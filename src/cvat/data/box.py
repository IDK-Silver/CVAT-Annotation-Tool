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
        將邊界框轉換為 YOLO 格式：(x_center, y_center, width, height)
        所有值都被歸一化到 [0, 1] 範圍內
        """
        x_min = box[Box.Keys.xtl]
        y_min = box[Box.Keys.ytl]
        x_max = box[Box.Keys.xbr]
        y_max = box[Box.Keys.ybr]

        # 計算中心點坐標和寬高
        x_center = (x_min + x_max) / (2 * image_width)
        y_center = (y_min + y_max) / (2 * image_height)
        width = (x_max - x_min) / image_width
        height = (y_max - y_min) / image_height

        def convert_to_str(attrs):
            if to_str:
                return ' '.join(map(str, attrs))
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
    def to_pascal_voc_format(box: dict, height: int, width: int) -> tuple:

        """
        將 YOLO 格式的框轉換為 Pascal VOC 格式: (xmin, ymin, xmax, ymax)
        """
        # 從 YOLO 格式轉換回絕對坐標
        x_center = box[Box.Keys.xtl] * width
        y_center = box[Box.Keys.ytl] * height
        box_width = box[Box.Keys.xbr] * width
        box_height = box[Box.Keys.ybr] * height

        # 計算 Pascal VOC 格式的坐標
        xmin = int(x_center - box_width / 2)
        ymin = int(y_center - box_height / 2)
        xmax = int(x_center + box_width / 2)
        ymax = int(y_center + box_height / 2)

        # 確保坐標在圖像範圍內
        xmin = max(0, min(xmin, width - 1))
        ymin = max(0, min(ymin, height - 1))
        xmax = max(0, min(xmax, width - 1))
        ymax = max(0, min(ymax, height - 1))

        return xmin, ymin, xmax, ymax
