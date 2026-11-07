from aircraft_part import AircraftPart
from exceptions import DuplicateIdError, ItemNotFoundError
from collections.abc import Iterator
import json
from dataclasses import asdict


class Catalog:
    def __init__(self):
        self._items: dict[str, AircraftPart] = {}

    def add(self, item: AircraftPart) -> None:
        if item.item_id in self._items:
            raise DuplicateIdError("Item с таким ID уже сущестувует!")
        self._items[item.item_id] = item

    def get(self, item_id: str) -> AircraftPart:
        if item_id not in self._items:
            raise ItemNotFoundError("Элемента с таким item_id не существует!")
        return self._items[item_id]

    def remove(self, item_id: str) -> None:
        if item_id not in self._items:
            raise ItemNotFoundError("Элемента с таким item_id не существует!")
        del self._items[item_id]

    def find_by_category(self, category: str) -> list[AircraftPart]:
        res = []

        for item in self._items.values():
            if item.category == category:
                res.append(item)

        return res

    def find_by_name(self, query: str) -> list[AircraftPart]:
        res = []
        query = query.casefold()

        for item in self._items.values():
            if query in item.name.casefold():
                res.append(item)

        return res

    def __len__(self) -> int:
        return len(self._items)

    def __contains__(self, item_id: str) -> bool:
        return item_id in self._items

    def __iter__(self) -> Iterator[AircraftPart]:
        """return-ит элементы в порядке добавления"""
        return iter(self._items.values())

    def save(self, path: str) -> None:
        dct = {"format_version": 1, "items": []}

        for item in self:
            dct["items"].append(asdict(item))

        with open(path, "w", encoding="utf-8") as f:
            json.dump(dct, f, ensure_ascii=False, indent=4)
