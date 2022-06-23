class PysonException(Exception):
    """ Base exception class for PysonDB """

    def __init__(self, message: str) -> None:
        self.message: str = message

    def __str__(self) -> str:
        return self.message

class UnknownKeyError(PysonException):
    """ Unknown key error """


class SchemaTypeError(PysonException):
    """ Schema type error """

class IdDoesNotExistError(PysonException):
    """ ID does not exist error """