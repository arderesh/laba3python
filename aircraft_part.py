from dataclasses import dataclass
from exceptions import InvalidItemErr

@dataclass
class AircraftPart:
    item_id: str
    name: str
    category: str
    year: int
    maker: str
    weight: float

    def __post_init__(self):
        if self.weight <= 0:
            raise InvalidItemErr("Некорректная масса!")
        if not self.item_id.strip():
            raise InvalidItemErr("Идентификатор не должен быть пустым!")
        if not self.name.strip():
            raise InvalidItemErr("Название не должно быть пустым!")
        if not self.category.strip():
            raise InvalidItemErr("Категория не должна быть пустой!")
        if not self.maker.strip():
            raise InvalidItemErr("Поле производитель не должно быть пустым!")
        if self.date <= 0:
            raise InvalidItemErr("Год не должен быть меньше или равен 0!")