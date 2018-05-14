#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @namespace pyfortified_requests

import logging
from logging_fortified import (LoggingFormat, LoggingOutput)

from pyfortified_requests import (
    __python_required_version__,
    RequestsFortified,
)
from pyfortified_requests.errors import (
    get_exception_message,
    print_traceback,
    RequestsFortifiedErrorCodes,
)
from pyfortified_requests.exceptions.custom import (
    RequestsFortifiedBaseError,
    RequestsFortifiedModuleError,
)
from pyfortified_requests.support import (
    base_class_name,
    mv_request_retry_excps_func,
    python_check_version,
    REQUEST_RETRY_EXCPS,
    REQUEST_RETRY_HTTP_STATUS_CODES,
)

log = logging.getLogger(__name__)
python_check_version(__python_required_version__)


class RequestsFortifiedUpload(object):
    __mv_request = None

    def __init__(
        self,
        logger_level=logging.INFO,
        logger_format=LoggingFormat.JSON,
        logger_output=LoggingOutput.STDOUT_COLOR
    ):
        self.mv_request = RequestsFortified(
            logger_format=logger_format,
            logger_level=logger_level,
            logger_output=logger_output
        )

    @property
    def logger(self):
        return self.mv_request.logger

    @property
    def mv_request(self):
        return self.__mv_request

    @mv_request.setter
    def mv_request(self, value):
        self.__mv_request = value

    def request(self, **kwargs):
        return self.mv_request.request(**kwargs)

    @property
    def built_request_curl(self):
        return self.mv_request.built_request_curl

    def request_upload_json_file(
        self,
        upload_request_url,
        upload_data_file_path,
        upload_data_file_size,
        is_upload_gzip,
        request_label=None,
        upload_timeout=None
    ):
        """Upload File to requested URL.

        :param upload_request_url:
        :param upload_data_file_path:
        :param upload_data_file_size:
        :param is_upload_gzip:
        :param request_label:
        :param upload_timeout:
        :return:
        """
        _request_label = "Request Upload JSON File"
        request_label = "{0}: {1}".format(request_label, _request_label)  if request_label is not None else _request_label

        request_retry_excps = REQUEST_RETRY_EXCPS
        request_retry_http_status_codes = REQUEST_RETRY_HTTP_STATUS_CODES

        upload_request_retry = {"timeout": 60, "tries": -1, "delay": 60}
        upload_request_headers = {'Content-Length': "{0}".format(upload_data_file_size)}

        if is_upload_gzip:
            upload_request_headers.update({'Content-Type': 'application/gzip'})
        else:
            upload_request_headers.update({'Content-Type': 'application/json; charset=utf8'})

        if upload_timeout:
            upload_request_retry["timeout"] = int(upload_timeout)

        upload_extra = {
            'upload_request_url': upload_request_url,
            'upload_data_file_path': upload_data_file_path,
            'upload_data_file_size': upload_data_file_size,
            'upload_request_retry': upload_request_retry,
            'upload_request_headers': upload_request_headers
        }

        log.info(
            "{0}: Start".format(request_label),
            extra=upload_extra
        )

        try:
            with open(upload_data_file_path, 'rb') as upload_fp:
                response = self.mv_request.request(
                    request_method='PUT',
                    request_url=upload_request_url,
                    request_params=None,
                    request_data=upload_fp,
                    request_retry=upload_request_retry,
                    request_headers=upload_request_headers,
                    request_retry_excps=request_retry_excps,
                    request_retry_http_status_codes=request_retry_http_status_codes,
                    request_retry_excps_func=mv_request_retry_excps_func,
                    allow_redirects=False,
                    build_request_curl=False,
                    request_label=request_label
                )

        except RequestsFortifiedBaseError as tmv_ex:
            tmv_ex_extra = tmv_ex.to_dict()
            tmv_ex_extra.update({'error_exception': base_class_name(tmv_ex)})
            log.error("{0}: Failed".format(request_label), extra=tmv_ex_extra)
            raise

        except Exception as ex:
            print_traceback(ex)

            log.error(
                "{0}: Failed: Unexpected".format(request_label),
                extra={
                    'error_exception': base_class_name(ex),
                    'error_details': get_exception_message(ex)
                }
            )

            raise RequestsFortifiedModuleError(
                error_message="{0}: Failed: Unexpected: {1}: {2}".format(request_label, base_class_name(ex), get_exception_message(ex)),
                errors=ex,
                error_code=RequestsFortifiedErrorCodes.REQ_ERR_UPLOAD_DATA
            )

        log.info(
            "{0}: Finished".format(request_label)
        )
        return response

    def request_upload_data(
        self,
        upload_request_url,
        upload_data,
        upload_data_size,
        request_label=None,
        upload_timeout=None,
        build_request_curl=False
    ):
        """Upload Data to requested URL.

        :param upload_request_url:
        :param upload_data:
        :param upload_data_size:
        :param upload_timeout:
        :return:
        """
        _request_label = 'Request Upload Data'
        request_label = "{0}: {1}".format(request_label, _request_label)  if request_label is not None else _request_label

        log.info(
            "{0}: Start".format(request_label),
            extra={
                'upload_data_size': upload_data_size,
                'upload_request_url': upload_request_url,
            }
        )

        request_retry_excps = REQUEST_RETRY_EXCPS
        request_retry_http_status_codes = REQUEST_RETRY_HTTP_STATUS_CODES

        upload_request_retry = {"timeout": 60, "tries": -1, "delay": 60}

        request_headers = {
            'Content-type': 'application/json; charset=utf8',
            'Accept': 'text/plain',
            'Content-Length': str(upload_data_size)
        }

        if upload_timeout:
            upload_request_retry["timeout"] = int(upload_timeout)

        try:
            response = self.mv_request.request(
                request_method='PUT',
                request_url=upload_request_url,
                request_params=None,
                request_data=upload_data,
                request_retry=upload_request_retry,
                request_retry_excps=request_retry_excps,
                request_retry_http_status_codes=request_retry_http_status_codes,
                request_retry_excps_func=mv_request_retry_excps_func,
                request_headers=request_headers,
                allow_redirects=False,
                build_request_curl=build_request_curl,
                request_label=request_label
            )
        except RequestsFortifiedBaseError as tmv_ex:
            tmv_ex_extra = tmv_ex.to_dict()
            tmv_ex_extra.update({'error_exception': base_class_name(tmv_ex)})

            log.error(
                "{0}: Failed".format(request_label),
                extra=tmv_ex_extra
            )
            raise

        except Exception as ex:
            print_traceback(ex)

            log.error(
                "{0}: Failed: Unexpected".format(request_label),
                extra={'error_exception': base_class_name(ex),
                       'error_details': get_exception_message(ex)}
            )
            raise RequestsFortifiedModuleError(
                error_message="{0}: Failed: Unexpected: {1}: {2}".format(request_label, base_class_name(ex), get_exception_message(ex)),
                errors=ex,
                error_code=RequestsFortifiedErrorCodes.REQ_ERR_UPLOAD_DATA
            )

        log.info("{0}: Finished".format(request_label))
        return response
