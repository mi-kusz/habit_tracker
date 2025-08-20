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


class MissingAuthData(AppException):
    def __init__(self):
        self.message = "Missing email or password"
        super().__init__(self.message)


class InvalidCredentials(AppException):
    def __init__(self):
        self.message = "Invalid credentials"
        super().__init__(self.message)