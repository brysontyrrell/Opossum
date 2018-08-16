import json
import logging
import os

from jsonschema import validate, ValidationError

from opossum.exc import APIBadRequest, APIForbidden
from opossum import g


def response(message, status_code):
    return {
        'isBase64Encoded': False,
        'statusCode': status_code,
        'body': json.dumps(message),
        'headers': {'Content-Type': 'application/json'}
    }


def validate_json(schema_name):
    with open(os.path.join('schemas', f'{schema_name}.json', 'r')) as f_obj:
        schema_request = json.load(f_obj)

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


def handler(lambda_handler):
    """Wraps around Lambda handler functions for API Gateway events.

    :param function lambda_handler: A Lambda handler function

    :return: Wrapped function
    :rtype: function
    """
    def wrapper(*args, **kwargs):
        logging.debug('Decorator invoked!')
        logging.debug(f'Args: {args}')
        logging.debug(f'Keyword Args: {kwargs}')

        g.event = args[0]
        g.context = args[1]

        try:
            message, code = lambda_handler(*args, **kwargs)
        except APIBadRequest as err:
            return response({'error': str(err)}, 400)
        except APIForbidden as err:
            return response({'error': str(err)}, 403)

        return response(message, code)

    return wrapper


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
