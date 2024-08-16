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
    pass
