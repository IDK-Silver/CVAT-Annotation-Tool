from typing import List, Union

class Attr:
    class Keys:
        name = 'attr-name'
        values = 'attr-value'

        def __init__(self):
            pass

    def __init__(self):
        pass

    @staticmethod
    def create_object() -> dict:
        obj = {
            Attr.Keys.name: '',
            Attr.Keys.values: [

            ]
        }
        return obj

    @staticmethod
    def get_values(attr: Union['Attr', dict]) -> List[str]:
        return attr[Attr.Keys.values]

    @staticmethod
    def get_name(attr: Union['Attr', dict]) -> str:
        return attr[Attr.Keys.name]
