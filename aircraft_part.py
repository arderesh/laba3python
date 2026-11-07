from dataclasses import dataclass

@dataclass
class AircraftPart:
    item_id: str
    name: str
    category: str
    date: int
    maker: str
    wheight: float

    def __post_init__(self):
        if self.wheight <= 0:
            raise ValueError("Некорректная масса!")

