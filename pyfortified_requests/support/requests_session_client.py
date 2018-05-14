#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @namespace pyfortified_requests

import logging
import requests
from requests.adapters import (HTTPAdapter, DEFAULT_POOLSIZE)
from urllib3.util.retry import Retry
from pyfortified_requests.support import (REQUEST_RETRY_HTTP_STATUS_CODES)
from pyfortified_requests.errors import (get_exception_message)

log = logging.getLogger(__name__)


class RequestsSessionClient(object):
    POOL_SIZE = DEFAULT_POOLSIZE
    request_buffer = []

    __session = None

    def __init__(self, retry_tries=3, retry_backoff=0.1, retry_codes=None, session=None):

        if session is not None:
            assert isinstance(session, requests.Session)
            self.session = session
        else:
            self.session = requests.Session()

            if retry_codes is None:
                retry_codes = set(REQUEST_RETRY_HTTP_STATUS_CODES)

            adapter = HTTPAdapter(
                max_retries=Retry(
                    total=retry_tries,
                    backoff_factor=retry_backoff,
                    status_forcelist=retry_codes,
                )
            )

            self.session.mount('http://', adapter)
            self.session.mount('https://', adapter)

    @property
    def session(self):
        return self.__session

    @session.setter
    def session(self, value):
        self.__session = value

    def request(self, request_method, request_url, **kwargs):
        extra_session_request = {'method': request_method, 'url': request_url}
        extra_session_request.update(kwargs)
        log.debug("Session Request: Details", extra=extra_session_request)
        try:
            return self.session.request(method=request_method, url=request_url, **kwargs)
        except Exception as ex:
            log.warning(
                "Session Request: Failed: %s" % get_exception_message(ex),
                extra=extra_session_request,
            )
            raise
