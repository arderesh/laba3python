class CatalogError(Exception):
    pass

class InvalidItemError(CatalogError):
    pass

class DuplicateIdError(CatalogError):
    pass

class ItemNotFoundError(CatalogError):
    pass