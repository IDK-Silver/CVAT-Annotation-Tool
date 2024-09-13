import copy
import os.path
import shutil
import typing
import warnings
import pathlib
from typing import List
import threading

import cv2

import cvat.core
from cvat.meta import Attr
from cvat.meta import Label
from cvat.data.box import Box
from cvat.data.image import Image
from cvat.utility.dataset import split_dataset


def export(
        key: str, metadata: list, images_data: list, output_path: str,
        images_path: str = None, rations: list = None, dataset_name: str = 'data',
        image_prefix: str = '',
        names_map: dict = [],
        ignore_label: list = []
):
    images_data = copy.deepcopy(images_data)
    output_path: pathlib.Path = pathlib.Path(output_path).absolute() / dataset_name

    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)

    images_path = pathlib.Path(images_path).absolute()


    # all label name of main key
    all_label = []

    # get all label by metadata
    # check key is original or not
    if key == cvat.core.CVAT.default_key:
        # append all label name
        for label in metadata:
            label_name = label[Label.Keys.name]

            # add label to label list if not in ignore list
            if label_name not in ignore_label:
                all_label.append(
                    label[Label.Keys.name]
                )
    else:
        for attr in Label.get_attrs(metadata[0]):

            # append all name by label value
            if Attr.get_name(attr) == key:
                all_label = Attr.get_values(attr)

                # delete label by ignore list
                all_label = list(
                    set(all_label).difference(set(ignore_label))
                )
                break

    # label map to id
    # Ex : Cat: 0, Dog: 1, Kano: 2
    id_dict = {}

    # create map
    with open((output_path / 'obj.name'), 'a+') as objname_file:
        offset = 0
        objname_file.seek(0)
        if os.path.exists(output_path / 'obj.name'):
            for line in objname_file:
                id_dict[line.strip()] = offset
                offset += 1

        for index, label in enumerate(all_label):

            if label in id_dict.keys():
                continue

            id_dict[label] = offset + index
            objname_file.write(label + '\r\n')

    annotations = ['train', 'validation', 'test']
    ration = 0.

    for index, annotation in enumerate(annotations):

        # split image data
        ration += rations[index]
        sub_images, images_data = split_dataset(images_data, split_ratio=ration)

        # ensure folder is exists
        object_directory = output_path / str(annotation)
        os.makedirs(object_directory, exist_ok=True)

        for label in id_dict.keys():
            label_name = label
            if label_name in names_map.keys():
                label_name = names_map[label_name]
            os.makedirs(object_directory / label_name, exist_ok=True)

        threads = []

        for thread_index, image in enumerate(sub_images):
            image_filename = pathlib.Path(image[Image.Keys.name])
            threads.append(
                threading.Thread(target=__export_image_by_boxs, args= (
                        images_path, image_filename, object_directory, image_prefix, image, ignore_label,
                        id_dict, annotation, names_map
                    )
                )
            )
            threads[thread_index].start()

        for thread_index in range(len(threads)):
            threads[thread_index].join()


def __export_image_by_boxs(
        images_path: pathlib.Path, image_filename: pathlib.Path,
        object_directory: pathlib.Path, image_prefix: pathlib.Path, image: Image,
        ignore_label: typing.List[str], id_dict: dict, annotation: str,
        names_map: dict
):
    image_src = images_path / image_filename
    image_dst = object_directory / (image_prefix + image_filename.name)

    if not os.path.exists(image_src):
        print('cant find image : ', image_src)
        return

    img = cv2.imread(image_src)

    for index, box in enumerate(Image.get_boxs(image)):

        # if label in ignore list then pass
        if box[Box.Keys.label] in ignore_label:
            continue

        x_min = int(box[Box.Keys.xtl])
        y_min = int(box[Box.Keys.ytl])
        x_max = int(box[Box.Keys.xbr])
        y_max = int(box[Box.Keys.ybr])

        box_range_image = img[y_min:y_max, x_min:x_max]
        if box_range_image.size == 0:
            continue

        label_name = box[Box.Keys.label]
        if label_name in names_map.keys():
            label_name = names_map[label_name]

        cv2.imwrite(
            object_directory / label_name
            / (image_dst.stem + str(index) + '_' + image_dst.suffix), box_range_image)

