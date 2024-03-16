from functools import wraps

from django.http import HttpResponseNotAllowed


def require_GET(func):
    @wraps(func)
    async def check_method(request):
        if request.method != 'GET':
            return HttpResponseNotAllowed(('GET',))

        return await func(request)

    return check_method


def require_POST(func):
    @wraps(func)
    async def check_method(request):
        if request.method != 'POST':
            return HttpResponseNotAllowed(('POST',))

        return await func(request)

    return check_method


def require_DELETE(func):
    @wraps(func)
    async def check_method(request):
        if request.method != 'DELETE':
            return HttpResponseNotAllowed(('DELETE',))

        return await func(request)

    return check_method
