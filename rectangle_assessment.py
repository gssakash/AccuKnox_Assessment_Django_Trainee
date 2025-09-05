from typing import Iterator, Dict
class Rectangle:
    def __init__(self, length:int, width:int):
        self.length=length
        self.width=width

    def __iter__(self) -> Iterator[Dict[str, int]]:
        yield {'length' : self.length}
        yield {'width' : self.width}


rectangle_class_instance = Rectangle(length=4, width=8)
for iterator in rectangle_class_instance:
    print(iterator)