import os.path
import warnings
import pathlib
from typing import List

import cvat.core
from cvat.meta import Attr
from cvat.meta import Label
from cvat.image.box import Box
from cvat.image.image import Image


def export(
        key: str, metadata: list, images_data: list, output_path: str,
        images_path: str = None, proportion: list = None, dataset_name: str = 'data'
):

    images_abs_path: List[str] = []

    images_path = pathlib.Path(images_path).absolute()

    if images_path is not None:
        if os.path.exists(images_path):
            images_path = [f for f in os.listdir(images_path) if os.path.isfile(images_path / f)]
            if len(images_path) <= 0:
                warnings.warn('yolo input image path is not exists any file')
        else:
            warnings.warn('yolo loading image error : path is not exists')

    # all label name of main key
    all_label = []

    # get all label by metadata
    # check key is original or not
    if key == cvat.core.CVAT.default_key:

        # append all label name
        for label in metadata:
            all_label.append(
                label[Label.Keys.name]
            )
    else:
        for attr in Label.get_attrs(metadata[0]):

            # append all name by label value
            if Attr.get_name(attr) == key:
                all_label = Attr.get_values(attr)
                break

    # label map to id
    # Ex : Cat: 0, Dog: 1, Kano: 2
    id_dict = {}

    # create map
    for index, label in enumerate(all_label):
        id_dict[label] = index

    # get all image info
    for image in images_data:

        # get box info from image
        for box in Image.get_boxs(image):
            pass


    print(images_path)
    # print(
    #     Box.to_yolo_format(
    #         box=box,
    #         image_width=image[Image.Keys.width],
    #         image_height=image[Image.Keys.height],
    #         cls_id=id_dict[box[Box.Keys.label]], to_str=True)
    # )
