from aircraft_part import AircraftPart
from catalog import Catalog
from dataclasses import asdict
import json



with open("catalog.json", "r", encoding="utf-8") as f:
    doc = json.load(f)

# dct = {"format_version": 1,
#        "items": []}
# first = AircraftPart(item_id="ID-1", name="Лопатка турбины",
#                          category="Двигатель", year=2020,
#                          maker="GE", weight=5.5)
# second = AircraftPart(item_id="ID-2", name="Диск турбины",
#                           category="Двигатель", year=2020,
#                           maker="GE", weight=10.0)
# catal = Catalog()
# catal.add(first)
# catal.add(second)
#
# for item in catal:
#     dct["items"].append(asdict(item))
#
# with open("catalog.json", "w", encoding="utf-8") as f:
#     json.dump(dct, f, ensure_ascii=False, indent=4)


# print(dct)