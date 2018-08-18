class OpossumException(Exception):
    pass


class APIException(OpossumException):
    """Base API Exception"""
    status_code = 0


class APIBadRequest(APIException):
    """400 Error"""
    status_code = 400


class APIForbidden(APIException):
    """403 Error"""
    status_code = 403


class APINotFound(APIException):
    """404 Error"""
    status_code = 404


class SchemaNotFound(OpossumException):
    pass
