DATE_FORMAT = '%d.%m.%Y'
DATETIME_FORMAT = '%Y.%m.%d %H:%M:%S'
TIME_FORMAT = '%H:%M:%S'
TIME_SHORT_FORMAT = '%H:%M'
DATETIME_FORMAT_FULL = '%Y.%m.%d %H:%M:%S.%f%z'


class DataKeys:
    SUCCESS = 'success'
    SUCCESS_b = SUCCESS.encode()

    RESULT = 'result'
    RESULT_b = RESULT.encode()

    ERRORS = 'errors'

    SUCCESS_RESPONSE_PREFIX = b'{"' + SUCCESS_b + b'":true,"' + RESULT_b + b'":'
    SUCCESS_RESPONSE_POSTFIX = b'}'


class Errors:
    ERROR_404 = '404 (Объект не найден)'

    INTERNAL_SERVER_ERROR = '500 INTERNAL_SERVER_ERROR'
    NOT_IMPLEMENTED = '501 NOT IMPLEMENTED'

    SERVER_ADDRESS_ERROR = 'Server address format error. Need like "ip:port"'
