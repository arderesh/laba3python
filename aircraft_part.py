from dataclasses import dataclass
from exceptions import InvalidItemError

@dataclass
class AircraftPart:
    item_id: str
    name: str
    category: str
    year: int
    maker: str
    weight: float

    def __post_init__(self):
        if not isinstance(self.item_id, str):
            raise InvalidItemError("item_id должен быть строкой")
        if not isinstance(self.name, str):
            raise InvalidItemError("name должно быть строкой")
        if not isinstance(self.category, str):
            raise InvalidItemError("category должно быть строкой")
        if not isinstance(self.maker, str):
            raise InvalidItemError("maker должно быть строкой")
        if type(self.year) != int:
            raise InvalidItemError("year должен иметь тип int")
        if type(self.weight) not in (int, float):
            raise InvalidItemError("weight должен иметь тип int или float")

        if self.weight <= 0:
            raise InvalidItemError("Некорректная масса!")
        if not self.item_id.strip():
            raise InvalidItemError("Идентификатор не должен быть пустым!")
        if not self.name.strip():
            raise InvalidItemError("Название не должно быть пустым!")
        if not self.category.strip():
            raise InvalidItemError("Категория не должна быть пустой!")
        if not self.maker.strip():
            raise InvalidItemError("Поле производитель не должно быть пустым!")
        if self.year <= 0:
            raise InvalidItemError("Год не должен быть меньше или равен 0!")