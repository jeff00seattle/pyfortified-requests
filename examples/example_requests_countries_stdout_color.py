#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging

from pprintpp import pprint
from requests_fortified import (
    RequestsFortifiedDownload,
)
from requests_fortified.support import (
    HEADER_CONTENT_TYPE_APP_JSON
)
from logging_fortified import (
    LoggingFormat,
    LoggingOutput
)

URL_REST_COUNTRIES = \
    'https://restcountries.eu/rest/v2/all'

request_download = RequestsFortifiedDownload(
    logger_level=logging.DEBUG,
    logger_output=LoggingOutput.STDOUT_COLOR,
    logger_format=LoggingFormat.JSON,
)

request_download.logger.note(request_download.logger.getLevelName().lower())
request_download.logger.info("Start".upper())

result = \
    request_download.request(
        request_method='GET',
        request_url=URL_REST_COUNTRIES,
        request_params=None,
        request_retry=None,
        request_headers=HEADER_CONTENT_TYPE_APP_JSON,
        request_label="REST Countries"
    )

request_download.logger.info("Completed".upper(), extra=vars(result))

json_rest_countries = result.json()
pprint(json_rest_countries)