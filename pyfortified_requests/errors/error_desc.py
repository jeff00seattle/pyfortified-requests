#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @namespace pyfortified_requests

from pyhttpstatus_utils import HTTP_STATUS_DESC_DICT
from pyhttpstatus_utils import HTTP_STATUS_PHRASE_DICT

REQUESTS_FORTIFIED_ERROR_NAME_DICT = {
    -1: 'Unassigned',
    0: 'Success',
    600: 'Module Error',
    601: 'Argument Error',
    602: 'Request Error',
    603: 'Software Error',
    604: 'Unexpected Value',
    605: 'Request HTTP',
    606: 'Request Connect',
    607: 'Request Redirect',
    608: 'Retry Exhausted',
    609: 'Unexpected content-type returned',
    610: 'Upload Data Error',
    611: 'Auth Error',
    612: 'Auth JSON Error',
    613: 'Auth Response Error',
    614: 'JSON Decoding Error',
    699: 'Unexpected Error'
}

REQUESTS_FORTIFIED_ERROR_DESC_DICT = {
    -1: 'Unassiged exit condition',
    0: 'Successfully completed',
    600: 'Error occurred somewhere within module',
    601: 'Invalid or missing argument provided',
    602: 'Unexpected request failure',
    603: 'Unexpected software error was detected',
    604: 'Unexpected value returned',
    605: 'Request HTTP error occurred',
    606: 'Request Connection error occurred',
    607: 'Request Redirect',
    608: 'Retry Exhausted',
    609: 'Unexpected content-type returned',
    610: 'Upload Data Error',
    611: 'Auth Error',
    612: 'Auth JSON Error',
    613: 'Auth Response Error',
    614: 'JSON Decoding Error',
    699: 'Unexpected Error'
}


def error_name(error_code, return_bool=False):
    """Provide definition of Error Code

    Args:
        error_code:

    Returns:

    """
    if error_code is None or not isinstance(error_code, int):
        return "Error Code: Invalid Type: %d" % error_code

    exit_code_name_ = HTTP_STATUS_PHRASE_DICT.get(error_code, None)
    if exit_code_name_ is not None:
        return exit_code_name_

    exit_code_name_ = REQUESTS_FORTIFIED_ERROR_NAME_DICT.get(error_code, None)
    if exit_code_name_ is not None:
        return exit_code_name_

    return False if return_bool else "Error Code: Undefined: %d" % error_code


def error_desc(error_code, return_bool=False):
    """Provide definition of Error Code

    Args:
        error_code:

    Returns:

    """
    if error_code is None or not isinstance(error_code, int):
        return "Error Code: Invalid Type: %d" % error_code

    exit_code_description_ = HTTP_STATUS_DESC_DICT.get(error_code, None)
    if exit_code_description_ is not None:
        return exit_code_description_

    exit_code_description_ = REQUESTS_FORTIFIED_ERROR_DESC_DICT.get(error_code, None)
    if exit_code_description_ is not None:
        return exit_code_description_

    return False if return_bool else "Error Code: Undefined: %d" % error_code
