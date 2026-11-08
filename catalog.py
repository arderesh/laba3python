from aircraft_part import AircraftPart
from exceptions import DuplicateIdError, ItemNotFoundError, InvalidItemError
from exceptions import UnsuportedVersion, BrokenFileError
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
        """выводит элементы в порядке добавления"""
        return iter(self._items.values())

    def save(self, path: str) -> None:
        dct = {"format_version": 1, "items": []}

        for item in self:
            dct["items"].append(asdict(item))

        with open(path, "w", encoding="utf-8") as f:
            json.dump(dct, f, ensure_ascii=False, indent=4)

    def load(self, path: str) -> None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                doc = json.load(f)
        except json.JSONDecodeError as error:
            raise BrokenFileError("Некорректный JSON") from error

        if not isinstance(doc, dict):
            raise BrokenFileError("Файл поврежден!")

        if "format_version" not in doc or "items" not in doc:
            raise BrokenFileError("Файл поврежден! Отсутствуют ключи format_version или items!")

        if type(doc["format_version"]) != int:
            raise BrokenFileError("Файл поврежден! Значение ключа format_version должно иметь тип int!")

        if type(doc["items"]) != list:
            raise BrokenFileError("Файл поврежден! Значение ключа items должно быть списком!")

        if doc["format_version"] != 1:
            raise UnsuportedVersion("Другая версия формата!")

        new = Catalog()
        for item in doc["items"]:
            if not isinstance(item, dict):
                raise BrokenFileError("Каждый элемент Items должен быть словарем!")
            try:
                new.add(AircraftPart(**item))
            except (TypeError, InvalidItemError, DuplicateIdError) as error:
                raise BrokenFileError("Некорректная запись детали") from error

        self._items = new._items