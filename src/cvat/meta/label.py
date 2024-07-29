from typing import List, Union
from .attr import Attr


class Label:
    class Keys:
        name = 'label-name'
        type = 'label-type'
        attrs = 'label-attrs'

        def __init__(self):
            pass

    def __init__(self):
        pass

    @staticmethod
    def create_object() -> dict:
        obj = {
            Label.Keys.name: '',
            Label.Keys.type: '',
            Label.Keys.attrs: [
            ]
        }
        return obj

    @staticmethod
    def get_attrs(lab: Union['Label', dict]) -> List[Attr]:
        return lab[Label.Keys.attrs]
