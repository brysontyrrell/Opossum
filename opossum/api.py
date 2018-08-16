import json
import logging
import os

from jsonschema import validate, ValidationError

from opossum.exc import APIBadRequest, APIForbidden, SchemaNotFound
from opossum import g

_LAMBDA_ROOT = os.getenv('LAMBDA_TASK_ROOT')


def response(message, status_code):
    return {
        'isBase64Encoded': False,
        'statusCode': status_code,
        'body': json.dumps(message),
        'headers': {'Content-Type': 'application/json'}
    }


def validate_json(schema_name):
    try:
        schema_path = os.path.join(
            _LAMBDA_ROOT, 'schemas', f'{schema_name}.json')

        with open(schema_path, 'r') as f_obj:
            schema_request = json.load(f_obj)
    except IOError:
        raise SchemaNotFound(f'Could not load a schema for {schema_name}')

    try:
        request_data = json.loads(g.event['body'])
    except (TypeError, json.JSONDecodeError):
        logging.exception('Bad Request: No JSON content found')
        raise APIBadRequest('Bad Request: No JSON content found')

    try:
        validate(request_data, schema_request)
    except ValidationError:
        logging.exception(
            'Bad Request: One or more required fields are missing or invalid')
        raise APIBadRequest(
            'One or more required fields are missing or invalid')


def handler(lambda_handler=None, json_validation=None):
    """Wraps around Lambda handler functions for API Gateway events.

    :param function lambda_handler: A Lambda handler function
    :param str json_validation: (Optional) The name of a schema file located in
        a ``schemas`` directory to validate a request's JSON payload against.

    :return: Wrapped function
    :rtype: function
    """
    def decorator(lambda_handler):

        def wrapper(*args, **kwargs):
            g.event = args[0]
            g.context = args[1]

            try:
                if json_validation:
                    validate_json(json_validation)

                message, code = lambda_handler(*args, **kwargs)

            except APIBadRequest as err:
                return response({'message': str(err)}, 400)
            
            except APIForbidden as err:
                return response({'message': str(err)}, 403)

            return response(message, code)

        return wrapper

    return decorator(lambda_handler) if lambda_handler else decorator


# def api_opts(func=None, validate=None):
#     def decorator(func):
#         if validate:
#             validate_json(validate)
#
#         def inner(*args, **kwargs):
#             return ('{colour_open}<b>{message}</b>{colour_close}'
#                     .format(colour_open=colour_open,
#                             colour_close=colour_close,
#                             message=func(*args, **kwargs)))
#         return inner
#
#     return decorator(func) if func is not None else decorator
