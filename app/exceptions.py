class AppException(Exception):
    pass


class EntityNotFoundException(AppException):
    def __init__(self, entity_type: str):
        self.message = f"{entity_type} not found"
        super().__init__(self.message)


class EntityPersistenceException(AppException):
    def __init__(self, entity_type: str):
        self.message = f"{entity_type} cannot be added to the database"
        super().__init__(self.message)