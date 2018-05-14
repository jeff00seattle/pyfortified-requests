#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @namespace pyfortified_requests

import logging
import requests

from pyfortified_requests import (
    __python_required_version__,
)
from pyfortified_requests.errors import (
    get_exception_message,
    RequestsFortifiedErrorCodes,
)
from pyfortified_requests.exceptions.custom import (
    RequestsFortifiedBaseError,
)
from pyfortified_requests.support.utils import (
    base_class_name,
    python_check_version,
)

log = logging.getLogger(__name__)
python_check_version(__python_required_version__)


def mv_request_retry_excps_func(excp, request_label=None):
    """Request Retry Exception Function

    :param excp:
    :param request_label:
    :return:
    """
    _request_label = 'Request Upload Exception'
    request_label = '{}: {}'.format(request_label, _request_label) if request_label is not None else _request_label

    error_exception = base_class_name(excp)
    error_details = get_exception_message(excp)

    if isinstance(excp, RequestsFortifiedBaseError):
        log.debug(
            "{0}: Expected".format(request_label),
            extra={
                'error_exception': error_exception,
                'error_details': error_details,
            }
        )
    else:
        log.debug(
            "{0}: Unexpected".format(request_label),
            extra={
                'error_exception': error_exception,
                'error_details': error_details,
            }
        )

    if isinstance(excp, requests.exceptions.ConnectionError):
        if error_details.find('RemoteDisconnected') >= 0 or error_details.find('ConnectionResetError') >= 0:
            log.debug(
                "{0}: Retry".format(request_label),
                extra={
                    'error_exception': error_exception,
                    'error_details': error_details,
                }
            )
            return True

    if isinstance(excp, RequestsFortifiedBaseError) and excp.error_code == RequestsFortifiedErrorCodes.REQ_ERR_REQUEST_CONNECT:
        if error_details.find('RemoteDisconnected') >= 0 or error_details.find('ConnectionResetError') >= 0:
            log.debug(
                "{0}: Retry".format(request_label),
                extra={
                    'error_exception': error_exception,
                    'error_details': error_details,
                }
            )
            return True

    log.debug(
        "{0}: No Retry".format(request_label),
        extra={
            'error_exception': error_exception,
            'error_details': error_details,
        }
    )
    return False
