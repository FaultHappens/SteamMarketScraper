from typing import List, Any


class ItemInfo:
    itemId: str
    floatValue: float
    link: str
    

    def __init__(self, itemId: str, floatValue: float, link:str) -> None:
        self.itemId = itemId
        self.floatValue = floatValue
        self.link = link
        

