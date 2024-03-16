import json

from django.core.handlers.asgi import ASGIRequest
from django.http import HttpResponse, HttpResponseNotAllowed

from backend.common.data import DataKeys, Errors


class RefreshResponse(HttpResponse):
    def __init__(self, request: ASGIRequest | None = None):
        content = {
            'refresh': True,
            'url': request.path,
        }

        if request.method == 'GET':
            content['data'] = request.GET.dict()
        elif request.method == 'POST':
            content['data'] = json.loads(request.body.decode('utf-8'))
        else:
            HttpResponseNotAllowed(('GET, POST',))

        HttpResponse.__init__(self, content, content_type='text/json')


class SuccessResponse(HttpResponse):
    def __init__(self, data=None):
        if isinstance(data, bytes):
            content = b''.join((DataKeys.SUCCESS_RESPONSE_PREFIX,
                                data, DataKeys.SUCCESS_RESPONSE_POSTFIX))
        else:
            content = json.dumps({
                DataKeys.SUCCESS: True,
                DataKeys.RESULT: data
            }, default=str)

        HttpResponse.__init__(self, content, content_type='text/json')


class ErrorResponse(HttpResponse):
    def __init__(self, data: dict | str | list = None, code=200):
        if isinstance(data, str):
            data = data
        if isinstance(data, list) or isinstance(data, dict):
            data = data

        data = data if data else {}

        content = json.dumps({
            DataKeys.SUCCESS: False,
            DataKeys.RESULT: None,
            DataKeys.ERRORS: data
        }, default=str)

        HttpResponse.__init__(self, content, content_type='text/json', status=code)


class Responses:
    NotFound = ErrorResponse(Errors.ERROR_404, code=404)

    Err500 = ErrorResponse(Errors.INTERNAL_SERVER_ERROR, code=500)

    Err501 = ErrorResponse(Errors.NOT_IMPLEMENTED, code=501)

    EmailNotVerified = ErrorResponse('Email is not verified')

    AuthenticationError = ErrorResponse('Authentication Error')

    TwoFaNotActive = ErrorResponse('2-FA not active')


def get_client_info(request):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '') or request.META.get('REMOTE_ADDR', '')
    ip_address = ip_address.split(', ')[0]
    user_agent = request.META['HTTP_USER_AGENT']
    return ip_address, user_agent
