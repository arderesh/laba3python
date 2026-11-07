from aircraft_part import AircraftPart
from exceptions import DuplicateIdErr, ItemNotFoundErr


class Catalog:
    def __init__(self):
        self._items: dict[str, AircraftPart] = {}

    def add(self, item: AircraftPart) -> None:
        if item.item_id in self._items:
            raise DuplicateIdErr("Item с таким ID уже сущестувует!")
        self._items[item.item_id] = item

    def get(self, item_id: str) -> AircraftPart:
        if item_id not in self._items:
            raise ItemNotFoundErr("Элемента с таким item_id не существует!")
        return self._items[item_id]

    def remove(self, item_id: str) -> None:
        if item_id not in self._items:
            raise ItemNotFoundErr("Элемента с таким item_id не существует!")
        del self._items[item_id]

    def find_by_category(self, category: str) -> list[AircraftPart]:
        res = []

        for item in self._items.values():
            if item.category == category:
                res.append(item)

        return res