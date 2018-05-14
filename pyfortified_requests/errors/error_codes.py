#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @namespace pyfortified_requests

from pyhttpstatus_utils import HttpStatusCode

class RequestsFortifiedErrorCodes(HttpStatusCode):

    REQ_ERR_UNASSIGNED = -1

    REQ_OK = 0  # Success process

    #
    # 6xx Request Fortified Errors
    #

    REQ_ERR_MODULE = 600  # Module Error

    REQ_ERR_ARGUMENT = 601
    # Invalid or missing argument provided discovered in this module.

    REQ_ERR_REQUEST = 602
    # Call to Python requests package has failed.

    REQ_ERR_SOFTWARE = 603
    # Exit code that means an internal software error was detected.

    REQ_ERR_UNEXPECTED_VALUE = 604
    # Unexpected value eitherreturned or null.

    REQ_ERR_REQUEST_HTTP = 605
    # An HTTP error occurred.

    REQ_ERR_REQUEST_CONNECT = 606
    # A Connection error occurred.

    REQ_ERR_REQUEST_REDIRECTS = 607

    REQ_ERR_RETRY_EXHAUSTED = 608  # Retry Exhausted

    REQ_ERR_UNEXPECTED_CONTENT_TYPE_RETURNED = 609  # Unexpected content-type returned

    REQ_ERR_UPLOAD_DATA = 610  # Error during data upload

    REQ_ERR_AUTH_ERROR = 611  # Auth Error
    REQ_ERR_AUTH_JSON_ERROR = 612  # Auth JSON Error
    REQ_ERR_AUTH_RESP_ERROR = 613  # Auth Response Error
    REQ_ERR_JSON_DECODING_ERROR = 614  # JSON Decoding Error

    REQ_ERR_CONNECT = 615  # Connection Error originating from a python builtins.py exception

    REQ_ERR_UNEXPECTED = 699  # Unexpected Error
