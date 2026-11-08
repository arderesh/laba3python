import unittest
from aircraft_part import AircraftPart
from exceptions import InvalidItemError, DuplicateIdError, ItemNotFoundError, UnsuportedVersion, BrokenFileError
from catalog import Catalog
from tempfile import TemporaryDirectory
from pathlib import Path
import json

class TestAircraft(unittest.TestCase):
    def test_valid(self):
        part = AircraftPart(item_id="ID-1", name="Лопатка турбины",
                            category="Двигатель", year=2026,
                            maker="GE", weight=5.5)

        self.assertEqual(part.item_id, "ID-1")
        self.assertEqual(part.weight, 5.5)

    def test_negative_wheight(self):
        with self.assertRaises(InvalidItemError):
            AircraftPart(item_id="ID-1", name="Лопасть",
                         category="Двигатель", year=2026,
                         maker="GE", weight=-5.5)


    def test_emty_id(self):
        with self.assertRaises(InvalidItemError):
            AircraftPart(item_id="  ", name="Лопасть",
                         category="Двигатель", year=2026,
                         maker="GE", weight=5.5)


class TestCatalog(unittest.TestCase):
    def test_add_get(self):
        catalog = Catalog()
        part = AircraftPart(item_id="ID-1", name="Лопасть",
                            category="Двигатель", year=2026,
                            maker="GE", weight=5.5)
        catalog.add(part)
        self.assertEqual(len(catalog), 1)

        part_in_catal = catalog.get("ID-1")
        self.assertIs(part_in_catal, part) # каталог возвращает искходную деталь

    def test_duplicate_id(self):
        catalog = Catalog()
        part1 = AircraftPart(item_id="ID-1", name="Лопасть 52",
                            category="Двигатель", year=2052,
                            maker="GE", weight=5.2)
        part2 = AircraftPart(item_id="ID-1", name="Диск 67",
                            category="Двигатель", year=2067,
                            maker="GE", weight=6.7)
        catalog.add(part1)
        with self.assertRaises(DuplicateIdError):
            catalog.add(part2)

        self.assertEqual(len(catalog), 1)
        self.assertIs(catalog.get("ID-1"), part1) # каталог не изменился

    def test_remove(self):
        catalog = Catalog()
        part = AircraftPart(item_id="ID-1", name="Лопасть",
                            category="Двигатель", year=2026,
                            maker="GE", weight=5.5)
        catalog.add(part)
        catalog.remove("ID-1")

        self.assertEqual(len(catalog), 0)

        self.assertNotIn("ID-1", catalog)

        with self.assertRaises(ItemNotFoundError):
            catalog.get("ID-1")

        with self.assertRaises(ItemNotFoundError):
            catalog.remove("ID-1")

    def test_find_by_name(self):
        catalog = Catalog()
        part1 = AircraftPart(item_id="ID-1", name="Лопасть турбины",
                            category="Двигатель", year=2026,
                            maker="GE", weight=5.5)
        part2 = AircraftPart(item_id="ID-2", name="Диск турбины",
                            category="Двигатель", year=2026,
                            maker="GE", weight=10.0)
        part3 = AircraftPart(item_id="ID-3", name="Лопасть вентилятора",
                            category="Двигатель", year=2026,
                            maker="GE", weight=7.5)

        catalog.add(part1)
        catalog.add(part2)
        catalog.add(part3)

        res = catalog.find_by_name("ЛоП")
        self.assertEqual(len(res), 2)
        self.assertIn(part1, res)
        self.assertIn(part3, res)

        res1 = catalog.find_by_name("КрЫл")
        self.assertEqual(len(res1), 0)

        res.clear()
        self.assertEqual(len(catalog), 3)

        res2 = catalog.find_by_name("ЛоП")
        self.assertEqual(len(res2), 2)
        self.assertIn(part1, res2)
        self.assertIn(part3, res2)

    def test_find_by_category(self):
        catalog = Catalog()
        part1 = AircraftPart(item_id="ID-1", name="Лопасть турбины",
                            category="Двигатель", year=2026,
                            maker="GE", weight=5.5)
        part2 = AircraftPart(item_id="ID-2", name="Диск турбины",
                            category="Двигатель", year=2026,
                            maker="GE", weight=10.0)
        part3 = AircraftPart(item_id="ID-3", name="Крыло",
                            category="Крыло", year=2026,
                            maker="GE", weight=7.5)
        catalog.add(part1)
        catalog.add(part2)
        catalog.add(part3)

        res = catalog.find_by_category("Двигатель")
        self.assertIn(part1, res)
        self.assertIn(part2, res)
        self.assertEqual(len(res), 2)

        res1 = catalog.find_by_category("Шасси")
        self.assertEqual(len(res1), 0)

        res.clear()
        self.assertEqual(len(catalog), 3)
        res = catalog.find_by_category("Двигатель")
        self.assertIn(part1, res)
        self.assertIn(part2, res)
        self.assertEqual(len(res), 2)

    def test_iter_place(self):
        catalog = Catalog()
        part1 = AircraftPart(item_id="ID-2", name="Лопасть турбины",
                            category="Двигатель", year=2026,
                            maker="GE", weight=5.5)
        part2 = AircraftPart(item_id="ID-1", name="Диск турбины",
                            category="Двигатель", year=2026,
                            maker="GE", weight=10.0)

        catalog.add(part1)
        catalog.add(part2)

        catal_a = list(catalog)
        self.assertEqual(catal_a, [part1, part2])

        catal_b = list(catalog)
        self.assertEqual(catal_b, [part1, part2])

    def test_json_save_load(self):
        catalog = Catalog()

        part1 = AircraftPart(item_id="ID-1", name="Лопасть турбины",
                            category="Двигатель", year=2026,
                            maker="GE", weight=5.5)
        part2 = AircraftPart(item_id="ID-2", name="Диск турбины",
                            category="Двигатель", year=2026,
                            maker="GE", weight=10.0)
        catalog.add(part1)
        catalog.add(part2)

        with TemporaryDirectory() as dir:
            path = Path(dir) / "catalog.json"
            catalog.save(str(path))

            new_catalog = Catalog()
            new_catalog.load(str(path))

            self.assertEqual(list(new_catalog), list(catalog))
            self.assertEqual(len(new_catalog), 2)
            self.assertIn("ID-1", new_catalog)
            self.assertIn("ID-2", new_catalog)

    def test_unsupported_ver(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "catalog.json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"format_version": 2, "items": []}, f,
                          ensure_ascii=False, indent=4)

            catalog = Catalog()
            with self.assertRaises(UnsuportedVersion):
                catalog.load(str(path))

    def test_broken_json(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "catalog.json"
            with open(path, "w", encoding="utf-8") as f:
                f.write("{")

            catalog = Catalog()
            with self.assertRaises(BrokenFileError):
                catalog.load(str(path))

