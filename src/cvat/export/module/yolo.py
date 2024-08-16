import copy
import os.path
import shutil
import warnings
import pathlib
from typing import List

import cvat.core
from cvat.meta import Attr
from cvat.meta import Label
from cvat.data.box import Box
from cvat.data.image import Image
from cvat.utility.dataset import split_dataset


def export(
        key: str, metadata: list, images_data: list, output_path: str,
        images_path: str = None, rations: list = None, dataset_name: str = 'data'
):
    images_data = copy.deepcopy(images_data)
    output_path: pathlib.Path = pathlib.Path(output_path).absolute() / dataset_name

    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)

    images_path = pathlib.Path(images_path).absolute()

    # if images_path is not None:
    #     if os.path.exists(images_path):
    #         images_path = [f for f in os.listdir(images_path) if os.path.isfile(images_path / f)]
    #         if len(images_path) <= 0:
    #             warnings.warn('yolo input image path is not exists any file')
    #     else:
    #         warnings.warn('yolo loading image error : path is not exists')

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
    with open((output_path / 'obj.name'), 'w+') as objname_file:
        for index, label in enumerate(all_label):
            id_dict[label] = index
            objname_file.write(label + '\r\n')

    annotations = ['train', 'val', 'test']
    sub_images_data = []
    ration = 0.
    for index, annotation in enumerate(annotations):

        ration += rations[index]
        record_file = output_path / str(annotation + '.txt')

        sub_images, images_data = split_dataset(images_data, split_ratio=ration)

        with open(record_file, 'w+') as record_file:

            object_directory = output_path / str('object_' + annotation + '_data')
            os.makedirs(object_directory, exist_ok=True)
            for image in sub_images:

                image_filename = pathlib.Path(image[Image.Keys.name])

                shutil.copy(
                    images_path / image_filename, object_directory / image_filename
                )

                record_file.write(
                    str(object_directory / image_filename) + '\r\n'
                )
                with open(object_directory / (image_filename.stem + '.txt'), 'w+') as annotation_file:
                    for box in Image.get_boxs(image):
                        annotation_file.write(
                            Box.to_yolo_format(
                                box=box,
                                image_width=image[Image.Keys.width],
                                image_height=image[Image.Keys.height],
                                cls_id=id_dict[box[Box.Keys.label]], to_str=True
                            ) + '\r\n'
                        )

