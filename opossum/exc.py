__all__ = ['APIException', 'APIBadRequest', 'APIForbidden']


class OpossumException(Exception):
    pass


class APIException(OpossumException):
    pass


class APIBadRequest(APIException):
    pass


class APIForbidden(APIException):
    pass


class SchemaNotFound(OpossumException):
    pass
