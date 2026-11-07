from aircraft_part import AircraftPart
from exceptions import DuplicateIdErr

class Catalog:
    def __init__(self):
        self._items: dict[str, AircraftPart] = {}

    def add(self, item: AircraftPart) -> None:
        if item.item_id in self._items:
            raise DuplicateIdErr("Item с таким ID уже сущестувует!")
        self._items[item._item_id] = item