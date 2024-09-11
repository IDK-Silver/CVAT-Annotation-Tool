import xml.etree.ElementTree as ET
import json
import warnings

from typing import List, Union, Any
import copy

from .meta.label import Label, LabelType
from .meta.attr import Attr
from .data.image import Image
from .data.box import Box
from .data.mask import Mask
from .export.annotation_type import ExportAnnotationType
from .export import module
from .utility.annotation import rle_to_yolo_rectangle, rle_to_voc_rectangle


class CVAT:
    support_version = 1.1
    default_key = 'original'

    def __init__(self):
        self.__main_key = self.default_key
        self.__meta: list = []
        self.__images: list = []

        self.__content: dict = {
            'meta': self.__meta,
            'images': self.__images
        }

    def __str__(self):
        str_content = copy.deepcopy(self.__content)
        
        for image in str_content['images']:
            mask_infos =  image[Image.Keys.masks]
            if mask_infos is not None:
                for mask_info in mask_infos:
                    if len(mask_info[Mask.Keys.rle]) >= 10:
                        mask_info[Mask.Keys.rle] = mask_info[Mask.Keys.rle][:10] + "..."
            
        print(str_content)
        return str(json.dumps(str_content, indent=4, ensure_ascii=False))

    def __getitem__(self, index):
        cvat_file = CVAT()
        cvat_file.__meta = self.__meta
        if isinstance(index, slice):
            start = index.start or 0
            stop = index.stop or len(self.__images)
            step = index.step or 1
            cvat_file.__images = self.__images[start:stop:step]
        else:
            cvat_file.__images = [self.__images[index]]
        
        cvat_file.__content['images'] = cvat_file.__images
        cvat_file.__content['meta'] = cvat_file.__meta
            
        return cvat_file
    
    def load(self, path: str):
        tree = ET.parse(path)
        root = tree.getroot()

        version = root.find('version').text

        if float(version) > self.support_version:
            warnings.warn('CVAT : not support version')

        labels_element = None
        
        if labels_element is None:
            try:
                labels_element = root.find('meta').find('project').find('labels')
            except:
                pass
            
        if labels_element is None:
            try:
                labels_element = root.find('meta').find('project').find('tasks').find('labels')
            except:
                pass
        
        if labels_element is None:
            try:
                labels_element = root.find('meta').find('job').find('labels')
            except:
                pass
        
        if labels_element is None:
            try:
                labels_element = root.find('meta').find('task').find('labels')
            except:
                pass
        
        if labels_element is None:
            warnings.warn('CVAT : not find labels')
            exit(-1)
            
        if labels_element is not None:
            for label_element in labels_element:

                label = Label.create_object()

                label[Label.Keys.name] = label_element.find('name').text
                label[Label.Keys.type] = label_element.find('type').text

                attrs_element = label_element.find('attributes')

                if attrs_element is not None:

                    for attr_element in attrs_element:
                        attr = Attr.create_object()

                        attr[Attr.Keys.name] = attr_element.find('name').text
                        attr[Attr.Keys.values] = attr_element.find('values').text.split()

                        label[Label.Keys.attrs].append(attr)

                self.__meta.append(label)

        # Parse images
        for image_element in root.findall('image'):
            image = Image.create_object()
            image[Image.Keys.id] = image_element.get('id')
            image[Image.Keys.name] = image_element.get('name')
            image[Image.Keys.width] = int(image_element.get('width'))
            image[Image.Keys.height] = int(image_element.get('height'))
            
            # Decode boxes
            for box_element in image_element.findall('box'):
                box = Box.create_object()
                box[Box.Keys.label] = box_element.get('label')
                box[Box.Keys.xtl] = float(box_element.get('xtl'))
                box[Box.Keys.ytl] = float(box_element.get('ytl'))
                box[Box.Keys.xbr] = float(box_element.get('xbr'))
                box[Box.Keys.ybr] = float(box_element.get('ybr'))

                for attr_element in box_element.findall('attribute'):
                    attr_name = attr_element.get('name')
                    attr_value = attr_element.text
                    box[Box.Keys.attributes][attr_name] = attr_value

                image[Image.Keys.boxes].append(box)

            # Decode masks
            for mask_element in image_element.findall('mask'):
                mask = Mask.create_object()
                mask[Mask.Keys.label] = mask_element.get('label')
                mask[Mask.Keys.source] = mask_element.get('source')
                mask[Mask.Keys.occluded] = mask_element.get('occluded')
                mask[Mask.Keys.rle] = mask_element.get('rle')
                mask[Mask.Keys.width] = int(mask_element.get('width'))
                mask[Mask.Keys.height] = int(mask_element.get('height'))
                mask[Mask.Keys.left] = int(mask_element.get('left'))
                mask[Mask.Keys.top] = int(mask_element.get('top'))
                
                image[Image.Keys.masks].append(mask)
                
            self.__images.append(image)

    def get_meta(self) -> List[Union[Label, dict]]:
        return self.__meta

    def get_images(self) -> List[Union[dict, Image]]:
        return self.__images

    def transpose(self, attr_name: str = 'original'):

        # transpose itself is equal nothing happened
        if self.__main_key == attr_name:
            return

        # set default attr
        attr_list = [self.default_key]

        # to get all attr in meta
        for lab in self.__meta:
            for attr in Label.get_attrs(lab):
                attr_list.append(
                    Attr.get_name(attr)
                )

        # check attr exists
        if attr_name not in attr_list:
            warnings.warn('CVAT not find attr name')
            exit(-1)

        # swap label-name, attr-name
        for image in self.get_images():

            for box in Image.get_boxs(image):
                original_label = box[Box.Keys.label]

                attr_value = box[Box.Keys.attributes][attr_name]

                box[Box.Keys.label] = attr_value
                box[Box.Keys.attributes][self.__main_key] = original_label
                box[Box.Keys.attributes].pop(attr_name)

        # set new main key
        self.__main_key = attr_name

    def export(
            self, export_path: str = 'data',
            export_type: Union[ExportAnnotationType, str] = ExportAnnotationType.yolo, export_args: tuple = None):

        # export yolo format
        if export_type is ExportAnnotationType.yolo:
            module.yolo.export(self.__main_key, self.__meta, self.__images, export_path, *export_args)

        if export_type is ExportAnnotationType.unet:
            module.unet.export(self.__main_key, self.__meta, self.__images, export_path, *export_args)
            
    def add_label(self, label: Label):
        self.__meta.append(label)
        
        
    def merge_label(self, dest_label: Label, atrr_name: str, src_label: Label, autoconvert: bool = True):
        # check params
        if dest_label is None or src_label is None or atrr_name is None:
            warnings.warn('CVAT : merge label failed, params is None')
            exit(-1)
        
        # get label name
        src_label_name: str = None
        dest_label_name: str = None
        
        if isinstance(src_label, dict):
            src_label_name = src_label[Label.Keys.name]
        else:
            src_label_name = src_label
        
        if isinstance(dest_label, dict):
            dest_label_name = dest_label[Label.Keys.name]
        else:
            dest_label_name = dest_label
        
        # get label
        src_label: Label = None
        dest_label: Label = None
        
        # find src label and dest label
        for label in self.__meta:
            if label[Label.Keys.name] == src_label_name:
                src_label = label
                
            if label[Label.Keys.name] == dest_label_name:
                dest_label = label
        
        # get dest label attrs
        dest_label_attrs = dest_label[Label.Keys.attrs]
        
        # ensure dest label has attr name
        if atrr_name not in Label.get_attr_names(dest_label):
            warnings.warn('CVAT : merge label failed, dest label not find attr name')
            exit(-1)
        
        # get dest label attr
        dest_attr = None

        for attr in dest_label_attrs:
            if attr[Attr.Keys.name] == atrr_name:
                dest_attr = attr
                break
        
        # ensure dest label attr has src label name
        if src_label_name not in dest_attr[Attr.Keys.values]:
            dest_attr[Attr.Keys.values].append(src_label_name)
        
        # convert to dest type
        if autoconvert:
            self.convert_label_type(dest_label[Label.Keys.type])
        
        if dest_label[Label.Keys.type] == LabelType.rectangle:
            
            target_boxes = []
            
            for image in self.__images:
                for box in image[Image.Keys.boxes]:
                    if box[Box.Keys.label] == src_label_name:
                        target_boxes.append(box)

            
            for box in target_boxes:
                
                box[Box.Keys.attributes][atrr_name] = src_label_name
                
                box[Box.Keys.label] = dest_label_name
                
                
        
        
        self.__meta.remove(src_label)
        
            
    def convert_label_type(self, new_type: LabelType):
        
        if new_type == LabelType.rectangle:
            
            need_convert_images = []
            
            for image in self.__images:
                if image[Image.Keys.boxes] is not None and image[Image.Keys.masks] is  None:
                    continue
                need_convert_images.append(image)
                
            for image in need_convert_images:
                
                masks = image[Image.Keys.masks]
                
                for mask in masks:
                    
                    box = Box.create_object()
                    box[Box.Keys.label] = mask[Mask.Keys.label]
                    points = rle_to_voc_rectangle(
                        mask[Mask.Keys.height], 
                        mask[Mask.Keys.width], 
                        mask[Mask.Keys.top], 
                        mask[Mask.Keys.left],
                        image[Image.Keys.height],
                        image[Image.Keys.width]
                    )
                    
                    # np.float32 to built-in float  
                    points = [
                        float(point) for point in points
                    ]
                    
                    box[Box.Keys.label] = mask[Mask.Keys.label]
                    box[Box.Keys.xtl] = points[0]
                    box[Box.Keys.ytl] = points[1]
                    box[Box.Keys.xbr] = points[2]
                    box[Box.Keys.ybr] = points[3]
                    
                    image[Image.Keys.boxes].append(box)
                
                image[Image.Keys.masks] = []
        
    


        
        
        