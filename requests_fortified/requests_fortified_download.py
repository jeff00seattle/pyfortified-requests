#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @namespace requests_fortified

import logging
import csv
import datetime as dt
import gzip
import http.client as http_client
import io
import ujson as json
import os
import re
import time

import requests
from logging_fortified import (LoggingFormat, LoggingOutput)
from pprintpp import pprint

from requests_fortified import (__python_required_version__)
from requests_fortified.errors import (get_exception_message, RequestsFortifiedErrorCodes)
from requests_fortified.exceptions.custom import (
    RequestsFortifiedModuleError,
)
from requests_fortified.support import (
    base_class_name,
    bytes_to_human,
    csv_skip_last_row,
    detect_bom,
    env_usage,
    handle_json_decode_error,
    python_check_version,
    remove_bom,
    validate_response,
)
from requests_fortified.support.curl import command_line_request_curl
from .requests_fortified import (RequestsFortified)
from safe_cast import safe_dict

log = logging.getLogger(__name__)

python_check_version(__python_required_version__)


class RequestsFortifiedDownload(object):

    __requests_client = None

    def __init__(
        self,
        logger_level=logging.INFO,
        logger_format=LoggingFormat.JSON,
        logger_output=LoggingOutput.STDOUT_COLOR,
        requests_client=None,
    ):
        self.requests_client = RequestsFortified(
            logger_format=logger_format,
            logger_level=logger_level,
            logger_output=logger_output,
            requests_client=requests_client
        )

    @property
    def logger(self):
        return self.requests_client.logger

    @property
    def session(self):
        return self.requests_client.session

    @property
    def requests_session_client(self):
        return self.requests_client.requests_session_client

    @property
    def requests_client(self):
        return self.__requests_client

    @requests_client.setter
    def requests_client(self, value):
        self.__requests_client = value

    def request(self, **kwargs):
        return self.requests_client.request(**kwargs)

    @property
    def built_request_curl(self):
        return self.requests_client.built_request_curl

    def request_csv_download(
        self,
        request_method,
        request_url,
        tmp_csv_file_name,
        tmp_directory,
        request_params=None,
        request_data=None,
        request_retry=None,
        request_retry_func=None,
        request_retry_excps=None,
        request_retry_http_status_codes=None,
        request_retry_excps_func=None,
        request_headers=None,
        request_auth=None,
        request_label=None,
        build_request_curl=True,
        allow_redirects=True,
        verify=True,
        skip_first_row=False,
        skip_last_row=False,
        read_first_row=False,
        csv_delimiter=',',
        csv_header=None,
        encoding_write=None,
        encoding_read=None,
        decode_unicode=False,
    ):
        """Download and Read CSV file.

        Args:
            request_method: request_method for the new :class:`Request` object.
            request_url: URL for the new :class:`Request` object.
            tmp_csv_file_name: Provide temporary name for downloaded CSV
            tmp_directory: Provide temporary directory to hold downloaded CSV
            request_params: (optional) Dictionary or bytes to be sent in the query
                string for the :class:`Request`.
            request_data: (optional) Dictionary, bytes, or file-like object to
                send in the body of the :class:`Request`.
            request_retry: (optional) Retry configuration.
            request_headers: (optional) Dictionary of HTTP Headers to
                send with the :class:`Request`.
            request_auth: (optional) Auth tuple to enable
                Basic/Digest/Custom HTTP Auth.
            allow_redirects: (optional) Boolean. Set to True if
                POST/PUT/DELETE redirect following is allowed.
            verify: (optional) whether the SSL cert will be verified. A
                CA_BUNDLE path can also be provided. Defaults to ``True``.
            skip_first_row: (optional) Skip first row if it does not contain
                column headers.
            skip_last_row: (optional) Skip first row if it does not contain
                column values.
            read_first_row: (optional) Read first row separate from data returned.
            csv_delimiter: (optional) Delimiter character, default comma ','.
            csv_header:
            encoding_write:
            encoding_read:
            decode_unicode:

        Returns:
            Generator containing CSV data by rows in JSON dictionary format.

        """
        _request_label = 'Request Download CSV File'
        request_label = "{0}: {1}".format(request_label, _request_label)  if request_label is not None else _request_label

        log.debug(
            "{0}: Start".format(request_label),
            extra={
                'request_url': request_url,
                'encoding_write': encoding_write,
                'encoding_read': encoding_read,
            }
        )

        timer_start = dt.datetime.now()

        _attempts = 0
        _tries = 60
        _delay = 10

        while _tries:
            _attempts += 1

            log.info(
                "{0}: Attempt: {1}".format(request_label, _attempts),
                extra={
                    'request_url': request_url,
                }
            )

            response = self.requests_client.request(
                request_method=request_method,
                request_url=request_url,
                request_params=request_params,
                request_data=request_data,
                request_retry=request_retry,
                request_retry_func=request_retry_func,
                request_retry_excps=request_retry_excps,
                request_retry_http_status_codes=request_retry_http_status_codes,
                request_retry_excps_func=request_retry_excps_func,
                request_headers=request_headers,
                request_auth=request_auth,
                build_request_curl=build_request_curl,
                allow_redirects=allow_redirects,
                verify=verify,
                stream=True,
                request_label=request_label
            )

            if response is None:
                log.error(
                    "{0}: No response".format(request_label),
                    extra={
                        'request_url': request_url,
                    }
                )

                raise RequestsFortifiedModuleError(
                    error_message="{0}: No response".format(request_label),
                    error_code=RequestsFortifiedErrorCodes.REQ_ERR_REQUEST,
                )

            http_status_code = response.status_code

            timer_end = dt.datetime.now()
            timer_delta = timer_end - timer_start
            response_time_secs = timer_delta.seconds
            response_headers = None

            if hasattr(response, 'headers'):
                response_headers = \
                    json.loads(
                        json.dumps(
                            dict(response.headers)
                        )
                    )

            log.debug(
                "{0}: Response Status".format(request_label),
                extra={
                    'http_status_code': http_status_code,
                    'response_time_secs': response_time_secs,
                    'response_url': response.url,
                    'response_headers': safe_dict(response_headers),
                }
            )

            (tmp_csv_file_path, tmp_csv_file_size) = self.download_csv(
                response,
                tmp_directory,
                tmp_csv_file_name,
                request_label=request_label,
                encoding_write=encoding_write,
                decode_unicode=decode_unicode
            )

            if tmp_csv_file_path is not None:
                break

            _tries -= 1
            if not _tries:
                log.error(
                    "{0}: Exhausted Retries".format(request_label),
                    extra={
                        'tries': _tries,
                        'request_url': request_url,
                    }
                )

                raise RequestsFortifiedModuleError(
                    error_message="{0}: Exhausted Retries".format(request_label),
                    error_code=RequestsFortifiedErrorCodes.REQ_ERR_RETRY_EXHAUSTED
                )

            log.info(
                "{0}: Performing Retry".format(request_label),
                extra={
                    'tries': _tries,
                    'delay': _delay,
                    'request_url': request_url,
                }
            )

            time.sleep(_delay)

        log.info(
            "{0}: Finished".format(request_label),
            extra={
                'file_path': tmp_csv_file_path,
                'file_size': bytes_to_human(tmp_csv_file_size),
                'encoding_read': encoding_read,
            }
        )

        log.debug(
            "{0}: Usage".format(request_label),
            extra=env_usage(tmp_directory),
        )

        with open(file=tmp_csv_file_path, mode='r', encoding=encoding_read) as csv_file_r:
            if read_first_row:
                csv_report_name = csv_file_r.readline()
                csv_report_name = re.sub('\"', '', csv_report_name)
                csv_report_name = re.sub('\n', '', csv_report_name)

                log.info(
                    "{0}: Report".format(request_label),
                    extra={'csv_report_name': csv_report_name},
                )
            elif skip_first_row:
                next(csv_file_r)

            csv_file_header = next(csv_file_r)
            csv_header_actual = \
                [h.strip() for h in csv_file_header.split(csv_delimiter)]

            csv_header_hr = []
            index = 0
            for column_name in csv_header_actual:
                csv_header_hr.append({'index': index, 'name': column_name})
                index += 1

            log.debug(
                "{0}: Content Header".format(request_label),
                extra={'csv_header': csv_header_hr},
            )

            csv_fieldnames = csv_header if csv_header else csv_header_actual
            csv_dict_reader = csv.DictReader(csv_file_r, fieldnames=csv_fieldnames, delimiter=csv_delimiter)

            if skip_last_row:
                for row in csv_skip_last_row(csv_dict_reader):
                    yield row
            else:
                for row in csv_dict_reader:
                    yield row

    def request_json_download(
        self,
        request_method,
        request_url,
        tmp_json_file_name,
        tmp_directory,
        request_params=None,
        request_data=None,
        request_retry=None,
        request_retry_func=None,
        request_retry_excps=None,
        request_retry_excps_func=None,
        request_headers=None,
        request_auth=None,
        request_label=None,
        build_request_curl=False,
        allow_redirects=True,
        verify=True,
        encoding_write=None,
        encoding_read=None,
    ):
        """Download and Read JSON file.

        Args:
            request_method: request_method for the new :class:`Request` object.
            request_url: URL for the new :class:`Request` object.
            tmp_json_file_name: Provide temporary name for downloaded CSV
            tmp_directory: Provide temporary directory to hold downloaded CSV
            request_params: (optional) Dictionary or bytes to be sent in the query
                string for the :class:`Request`.
            request_data: (optional) Dictionary, bytes, or file-like object to
                send in the body of the :class:`Request`.
            request_retry: (optional) Retry configuration.
            request_headers: (optional) Dictionary of HTTP Headers to
                send with the :class:`Request`.
            request_auth: (optional) Auth tuple to enable
                Basic/Digest/Custom HTTP Auth.
            build_request_curl: (optional) Build a copy-n-paste curl for command line
                that provides same request as this call.
            allow_redirects: (optional) Boolean. Set to True if
                POST/PUT/DELETE redirect following is allowed.
            verify: (optional) whether the SSL cert will be verified. A
                CA_BUNDLE path can also be provided. Defaults to ``True``.
            encoding_write:
            encoding_read:
            decode_unicode:

        Returns:
            Generator containing JSON data by rows in JSON dictionary format.

        """
        _request_label = "Request Download JSON File"
        request_label = "{0}: {1}".format(request_label, _request_label)  if request_label is not None else _request_label

        log.info(
            "{0}: Start".format(request_label),
            extra={
                'request_url': request_url,
                'encoding_write': encoding_write,
                'encoding_read': encoding_read,
            }
        )

        timer_start = dt.datetime.now()

        _attempts = 0
        _tries = 60
        _delay = 10

        while _tries:
            _attempts += 1

            log.debug(
                "{0}: Download".format(request_label),
                extra={
                    'attempts': _attempts,
                    'request_url': request_url,
                }
            )

            response = self.requests_client.request(
                request_method=request_method,
                request_url=request_url,
                request_params=request_params,
                request_data=request_data,
                request_retry=request_retry,
                request_retry_func=request_retry_func,
                request_retry_excps=request_retry_excps,
                request_retry_excps_func=request_retry_excps_func,
                request_headers=request_headers,
                request_auth=request_auth,
                build_request_curl=build_request_curl,
                allow_redirects=allow_redirects,
                verify=verify,
                stream=True,
                request_label=request_label
            )

            if response is None:
                log.error(
                    "{0}: No response".format(request_label),
                    extra={
                        'request_url': request_url,
                    }
                )

                raise RequestsFortifiedModuleError(
                    error_message="{0}: No response".format(request_label),
                    error_code=RequestsFortifiedErrorCodes.REQ_ERR_REQUEST
                )

            http_status_code = response.status_code

            timer_end = dt.datetime.now()
            timer_delta = timer_end - timer_start
            response_time_secs = timer_delta.seconds
            response_headers = None

            if hasattr(response, 'headers'):
                response_headers = \
                    json.loads(
                        json.dumps(
                            dict(response.headers)
                        )
                    )

            log.debug(
                "{0}: Response Status".format(request_label),
                extra={
                    'http_status_code': http_status_code,
                    'response_time_secs': response_time_secs,
                    'response_url': response.url,
                    'response_headers': safe_dict(response_headers),
                }
            )

            if not os.path.exists(tmp_directory):
                os.mkdir(tmp_directory)

            tmp_json_file_path = "{0}/{1}".format(tmp_directory, tmp_json_file_name)

            if os.path.exists(tmp_json_file_path):
                log.debug(
                    "{0}: Removing".format(request_label),
                    extra={'file_path': tmp_json_file_path},
                )
                os.remove(tmp_json_file_path)

            mode_write = 'wb' if encoding_write is None else 'w'

            log.debug(
                "{0}: Finished".format(request_label),
                extra={
                    'file_path': tmp_json_file_path,
                    'mode_write': mode_write,
                    'encoding_write': encoding_write,
                }
            )

            log.debug(
                "{0}: Usage".format(request_label),
                extra=env_usage(tmp_directory)
            )

            chunk_total_sum = 0

            with open(file=tmp_json_file_path, mode=mode_write, encoding=encoding_write) as json_raw_file_w:
                log.debug(
                    "{0}: Response Raw: Started".format(request_label),
                    extra={
                        'file_path': tmp_json_file_path,
                    }
                )

                _tries -= 1
                error_exception = None
                error_details = None
                chunk_size = 8192
                try:
                    raw_response = response.raw
                    while True:
                        chunk = raw_response.read(chunk_size, decode_content=True)
                        if not chunk:
                            break

                        chunk_total_sum += chunk_size

                        json_raw_file_w.write(chunk)
                        json_raw_file_w.flush()
                        os.fsync(json_raw_file_w.fileno())

                    log.debug(
                        "{0}: By Chunk: Completed".format(request_label),
                        extra={
                            'file_path': tmp_json_file_path,
                        }
                    )

                    break

                except requests.exceptions.ChunkedEncodingError as chunked_encoding_ex:
                    error_exception = base_class_name(chunked_encoding_ex)
                    error_details = get_exception_message(chunked_encoding_ex)

                    log.warning(
                        "{0}: Error: {1}".format(request_label, error_exception),
                        extra={
                            'error_details': error_details,
                            'chunk_total_sum': chunk_total_sum,
                        }
                    )

                    if not _tries:
                        log.error(
                            "{0}: Exhausted Retries: Error: {1}".format(request_label, error_exception),
                        )
                        raise

                except http_client.IncompleteRead as incomplete_read_ex:
                    error_exception = base_class_name(incomplete_read_ex)
                    error_details = get_exception_message(incomplete_read_ex)

                    log.warning(
                        "{0}: IncompleteRead".format(request_label),
                        extra={
                            'error_exception': error_exception,
                            'error_details': error_details,
                            'chunk_total_sum': chunk_total_sum,
                        }
                    )

                    if not _tries:
                        log.error(
                            "{0}: Exhausted Retries: Error: {1}".format(request_label, error_exception),
                        )
                        raise

                except requests.exceptions.RequestException as request_ex:
                    log.error(
                        "{0}: Request Exception".format(request_label),
                        extra={
                            'error_exception': base_class_name(request_ex),
                            'error_details': get_exception_message(request_ex),
                            'chunk_total_sum': chunk_total_sum,
                        }
                    )
                    raise

                except Exception as ex:
                    log.error(
                        "{0}: Unexpected Exception".format(request_label),
                        extra={
                            'error_exception': base_class_name(ex),
                            'error_details': get_exception_message(ex),
                            'chunk_total_sum': chunk_total_sum,
                        }
                    )
                    raise

                if not _tries:
                    log.error(
                        "{0}: Exhausted Retries".format(request_label),
                        extra={
                            'tries': _tries,
                            'request_url': request_url,
                        }
                    )

                    raise RequestsFortifiedModuleError(
                        error_message="{0}: Exhausted Retries: {1}".format(request_label, request_url),
                        error_request_curl=self.built_request_curl,
                        error_code=RequestsFortifiedErrorCodes.REQ_ERR_RETRY_EXHAUSTED
                    )

                log.info(
                    "{0}: Performing Retry".format(request_label),
                    extra={
                        'tries': _tries,
                        'delay': _delay,
                        'request_url': request_url,
                    }
                )

                time.sleep(_delay)

        tmp_json_file_size = os.path.getsize(tmp_json_file_path)
        bom_enc, bom_len, bom_header = detect_bom(tmp_json_file_path)

        log.info(
            "{0}: By Chunk: Completed: Details".format(request_label),
            extra={
                'file_path': tmp_json_file_path,
                'file_size': bytes_to_human(tmp_json_file_size),
                'chunk_total_sum': chunk_total_sum,
                'bom_encoding': bom_enc,
            }
        )

        if bom_enc == 'gzip':
            tmp_json_gz_file_path = "%s.gz" % tmp_json_file_path

            os.rename(src=tmp_json_file_path, dst=tmp_json_gz_file_path)

            with open(file=tmp_json_file_path, mode=mode_write, encoding=encoding_write) as json_file_w:
                log.debug(
                    "{0}: GZip: Started".format(request_label),
                    extra={
                        'file_path': tmp_json_file_path,
                    }
                )

                with gzip.open(tmp_json_gz_file_path, 'r') as gzip_file_r:
                    json_file_w.write(gzip_file_r.read())

        response_extra = {
            'file_path': tmp_json_file_path,
            'file_size': bytes_to_human(tmp_json_file_size),
        }

        log.info(
            "{0}: Read Downloaded".format(request_label),
            extra=response_extra
        )

        json_download = None
        with open(tmp_json_file_path, mode='r') as json_file_r:
            json_file_content = json_file_r.read()
            try:
                json_download = json.loads(json_file_content)
            except ValueError as json_decode_ex:
                pprint(json_file_content)

                response_extra.update({
                    'json_file_content': json_file_content,
                    'json_file_content_len': len(json_file_content)
                })

                handle_json_decode_error(
                    response_decode_ex=json_decode_ex,
                    response=response,
                    response_extra=response_extra,
                    request_label=request_label,
                    request_curl=self.built_request_curl
                )

            except Exception as ex:
                pprint(json_file_content)

                response_extra.update({
                    'json_file_content': json_file_content,
                    'json_file_content_len': len(json_file_content)
                })

                log.error(
                    "{0}: Failed: Exception".format(request_label),
                    extra=response_extra,
                )

                handle_json_decode_error(
                    response_decode_ex=ex,
                    response=response,
                    response_extra=response_extra,
                    request_label=request_label,
                    request_curl=self.built_request_curl
                )

        response_extra.update({'json_file_content_len': len(json_download)})

        log.info(
            "{0}: Finished".format(request_label),
            extra=response_extra
        )

        return json_download

    def download_csv(
        self,
        response,
        tmp_directory,
        tmp_csv_file_name,
        request_label=None,
        encoding_write=None,
        decode_unicode=False,
    ):
        _request_label = "Download CSV"
        request_label = "{0}: {1}".format(request_label, _request_label)  if request_label is not None else _request_label

        log.debug(
            "{0}: Start".format(request_label)
        )

        if not os.path.exists(tmp_directory):
            os.mkdir(tmp_directory)

        tmp_csv_file_path = "{0}/{1}".format(tmp_directory, tmp_csv_file_name)

        if os.path.exists(tmp_csv_file_path):
            log.debug(
                "{0}: Removing previous CSV".format(request_label),
                extra={'file_path': tmp_csv_file_path},
            )
            os.remove(tmp_csv_file_path)

        mode_write = 'wb' if encoding_write is None else 'w'

        log.debug(
            "{0}: Details".format(request_label),
            extra={
                'file_path': tmp_csv_file_path,
                'mode_write': mode_write,
                'encoding_write': encoding_write,
            }
        )

        chunk_total_sum = 0

        with open(file=tmp_csv_file_path, mode=mode_write, encoding=encoding_write) as csv_file_wb:
            log.debug(
                "{0}: By Chunk: Started".format(request_label),
                extra={
                    'file_path': tmp_csv_file_path,
                    'request_label': request_label
                }
            )

            error_exception = None
            error_details = None

            try:
                for chunk in response.iter_content(chunk_size=8192, decode_unicode=decode_unicode):
                    if not chunk:
                        break

                    chunk_total_sum += 8192

                    csv_file_wb.write(chunk)
                    csv_file_wb.flush()
                    os.fsync(csv_file_wb.fileno())

                log.debug(
                    "{0}: By Chunk: Completed".format(request_label),
                    extra={
                        'file_path': tmp_csv_file_path,
                    }
                )

            except requests.exceptions.ChunkedEncodingError as chunked_encoding_ex:
                error_exception = base_class_name(chunked_encoding_ex)
                error_details = get_exception_message(chunked_encoding_ex)

                log.warning(
                    "{0}: ChunkedEncodingError".format(request_label),
                    extra={
                        'error_exception': error_exception,
                        'error_details': error_details,
                        'chunk_total_sum': bytes_to_human(chunk_total_sum),
                    }
                )

                return (None, 0)

            except http_client.IncompleteRead as incomplete_read_ex:
                error_exception = base_class_name(incomplete_read_ex)
                error_details = get_exception_message(incomplete_read_ex)

                log.warning(
                    "{0}: IncompleteRead".format(request_label),
                    extra={
                        'error_exception': error_exception,
                        'error_details': error_details,
                        'chunk_total_sum': bytes_to_human(chunk_total_sum),
                    }
                )

                return (None, 0)

            except requests.exceptions.RequestException as request_ex:
                log.error(
                    "{0}: Request Exception".format(request_label),
                    extra={
                        'error_exception': base_class_name(request_ex),
                        'error_details': get_exception_message(request_ex),
                        'chunk_total_sum': bytes_to_human(chunk_total_sum),
                    }
                )
                raise

            except Exception as ex:
                log.error(
                    "{0}: Unexpected Exception".format(request_label),
                    extra={
                        'error_exception': base_class_name(ex),
                        'error_details': get_exception_message(ex),
                        'chunk_total_sum': bytes_to_human(chunk_total_sum),
                    }
                )
                raise

        tmp_csv_file_size = os.path.getsize(tmp_csv_file_path)
        bom_enc, bom_len, bom_header = detect_bom(tmp_csv_file_path)

        log.info(
            "{0}: By Chunk: Completed: Details".format(request_label),
            extra={
                'file_path': tmp_csv_file_path,
                'file_size': bytes_to_human(tmp_csv_file_size),
                'chunk_total_sum': bytes_to_human(chunk_total_sum),
                'bom_encoding': bom_enc
            }
        )

        log.debug(
            "{0}: Download CSV: Usage".format(request_label),
            extra=env_usage(tmp_directory)
        )

        tmp_csv_file_name_wo_ext = \
            os.path.splitext(
                os.path.basename(tmp_csv_file_name)
            )[0]

        tmp_csv_file_path_wo_bom = "{0}/{1}_wo_bom.csv".format(tmp_directory, tmp_csv_file_name_wo_ext)

        if os.path.exists(tmp_csv_file_path_wo_bom):
            os.remove(tmp_csv_file_path_wo_bom)

        bom_enc, bom_len = remove_bom(tmp_csv_file_path, tmp_csv_file_path_wo_bom)

        log.debug(
            "{0}: Encoding".format(request_label),
            extra={
                'bom_enc': bom_enc,
                'bom_len': bom_len
            }
        )

        if bom_len > 0:
            tmp_csv_file_path = tmp_csv_file_path_wo_bom

        return (tmp_csv_file_path, tmp_csv_file_size)

    def stream_csv(
        self,
        request_url,
        request_params,
        csv_delimiter=',',
        request_retry=None,
        request_headers=None,
        request_label=None,
        chunk_size=1024,
        decode_unicode=False,
        remove_bom_length=0
    ):
        """Stream CSV and Yield JSON

        Args:
            request_url:
            request_params:
            csv_delimiter:
            request_retry:
            request_headers:
            chunk_size:
            decode_unicode:
            remove_bom_length:

        Returns:

        """
        _request_label = "Stream CSV"
        request_label = "{0}: {1}".format(request_label, _request_label)  if request_label is not None else _request_label

        log.info(
            "{0}: Start".format(request_label),
            extra={'report_url': request_url}
        )

        response = self.requests_client.request(
            request_method='GET',
            request_url=request_url,
            request_params=request_params,
            request_retry=request_retry,
            request_headers=request_headers,
            stream=True,
            request_label="{0}: Request".format(request_label)
        )

        log.info(
            "{0}: Response".format(request_label),
            extra={
                'response_status_code': response.status_code,
                'response_headers': response.headers,
                'report_url': request_url
            }
        )

        request_curl = command_line_request_curl(
            request_method='GET',
            request_url=request_url,
            request_params=request_params,
            request_headers=request_headers,
        )

        validate_response(response=response, request_curl=request_curl, request_label="Stream CSV")

        response_content_type = response.headers.get('Content-Type', None)
        response_transfer_encoding = response.headers.get('Transfer-Encoding', None)
        response_http_status_code = response.status_code

        log.debug(
            "{0}: Status: Details".format(request_label),
            extra={
                'response_content_type': response_content_type,
                'response_transfer_encoding': response_transfer_encoding,
                'response_http_status_code': response_http_status_code
            }
        )

        log.debug("{0}: Usage".format(request_label), extra=env_usage())

        line_count = 0
        csv_keys_str = None
        csv_keys_list = None
        csv_keys_list_len = None
        pre_str_line = None

        for bytes_line in response.iter_lines(chunk_size=chunk_size, decode_unicode=decode_unicode):
            if bytes_line:  # filter out keep-alive new chunks
                line_count += 1

                str_line = bytes_line.decode("utf-8")
                if line_count == 1:
                    if remove_bom_length > 0:
                        str_line = str_line[remove_bom_length:]
                    csv_keys_list = str_line.split(csv_delimiter)
                    csv_keys_list = [csv_key.strip() for csv_key in csv_keys_list]
                    csv_keys_list_len = len(csv_keys_list)
                    continue

                if pre_str_line is not None:
                    str_line = pre_str_line + str_line
                    pre_str_line = None

                csv_values_str = str_line.replace('\n', ' ').replace('\r', ' ')

                csv_values_str_io = io.StringIO(csv_values_str)
                reader = csv.reader(csv_values_str_io, delimiter=csv_delimiter)
                csv_values_list = None
                for row in reader:
                    csv_values_list = row

                csv_values_list_len = len(csv_values_list)

                if csv_values_list_len < csv_keys_list_len:
                    pre_str_line = str_line
                    continue

                if csv_keys_list_len != csv_values_list_len:
                    log.error(
                        "{0}: Mismatch: CSV Key".format(request_label),
                        extra={
                            'line': line_count,
                            'csv_keys_list_len': csv_keys_list_len,
                            'csv_keys_str': csv_keys_str,
                            'csv_keys_list': csv_keys_list,
                            'csv_values_list_len': csv_values_list_len,
                            'csv_values_str': csv_values_str,
                            'csv_values_list': csv_values_list,
                        }
                    )
                    raise RequestsFortifiedModuleError(
                        error_message="{0}: Mismatch: CSV Key '{1}': Values '{2}'".format(request_label, csv_keys_str, csv_values_str),
                        error_code=RequestsFortifiedErrorCodes.REQ_ERR_UNEXPECTED_VALUE
                    )

                json_data_row = {}
                for idx, csv_key in enumerate(csv_keys_list):
                    csv_value = csv_values_list[idx]
                    json_data_row.update({csv_key: csv_value.strip('"')})

                yield json_data_row
