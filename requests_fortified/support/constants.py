#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @namespace requests_fortified

import sys
import requests
from requests_fortified import (__version__, __title__)
from pyhttpstatus_utils import (HttpStatusCode)

__all__ = [HttpStatusCode]

__MODULE_VERSION__ = __version__
__MODULE_VERSION_INFO__ = tuple(__MODULE_VERSION__.split('.'))
__MODULE_SIG__ = "%s/%s" % (__title__, __MODULE_VERSION__)

__TIMEZONE_NAME_DEFAULT__ = "UTC"

__PYTHON_VERSION__ = '%d.%d.%d' % (sys.version_info[0], sys.version_info[1], sys.version_info[2])
__PYTHON_SIG__ = "Python/%s" % __PYTHON_VERSION__

__USER_AGENT__ = "(%s, %s)" % (__MODULE_SIG__, __PYTHON_SIG__)

__LOGGER_NAME__ = __name__.split('.')[0]

HEADER_CONTENT_TYPE_APP_JSON = {'Content-Type': 'application/json'}
HEADER_CONTENT_TYPE_APP_URLENCODED = {'Content-Type': 'application/x-www-form-urlencoded'}

HEADER_USER_AGENT = \
    {'User-Agent': __USER_AGENT__}

REQUEST_RETRY_EXCPS = (
    requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.Timeout,
)

REQUEST_RETRY_HTTP_STATUS_CODES = [
    HttpStatusCode.INTERNAL_SERVER_ERROR,
    HttpStatusCode.BAD_GATEWAY,
    HttpStatusCode.SERVICE_UNAVAILABLE,
    HttpStatusCode.GATEWAY_TIMEOUT,
    HttpStatusCode.TOO_MANY_REQUESTS,
]

IRONIO_PARTITION = '/mnt/task'
