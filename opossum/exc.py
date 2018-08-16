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
