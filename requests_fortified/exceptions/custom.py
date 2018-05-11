#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @namespace requests_fortified

from requests_fortified.errors.error_codes import RequestsFortifiedErrorCodes
from requests_fortified.exceptions.base import (RequestsFortifiedBaseError)


class RequestsFortifiedError(RequestsFortifiedBaseError):
    pass


class RequestsFortifiedClientError(RequestsFortifiedBaseError):
    pass


class RequestsFortifiedServiceError(RequestsFortifiedBaseError):
    pass


class RequestsFortifiedModuleError(RequestsFortifiedBaseError):
    pass


class RequestsFortifiedClientGoneError(RequestsFortifiedModuleError):
    """Request Mv Integration: Value error"""

    def __init__(self, **kwargs):
        error_code = kwargs.pop('error_code', None) or \
                     RequestsFortifiedErrorCodes.GONE
        super(RequestsFortifiedClientGoneError, self).__init__(error_code=error_code, **kwargs)


class RequestsFortifiedValueError(RequestsFortifiedModuleError):
    """Request Mv Integration: Value error"""

    def __init__(self, **kwargs):
        error_code = kwargs.pop('error_code', None) or \
                     RequestsFortifiedErrorCodes.REQ_ERR_ARGUMENT
        super(RequestsFortifiedValueError, self).__init__(error_code=error_code, **kwargs)


class RequestsFortifiedAuthenticationError(RequestsFortifiedModuleError):
    """Request Mv Integration: Authentication error"""

    def __init__(self, **kwargs):
        error_code = kwargs.pop('error_code', None) or \
                     RequestsFortifiedErrorCodes.REQ_ERR_AUTH_ERROR
        super(RequestsFortifiedAuthenticationError, self).__init__(error_code=error_code, **kwargs)
