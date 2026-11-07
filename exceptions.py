class CatalogErr(Exception):
    pass

class InvalidItemErr(CatalogErr):
    pass

class DuplicateIdErr(CatalogErr):
    pass

class ItemNotFoundErr(CatalogErr):
    pass