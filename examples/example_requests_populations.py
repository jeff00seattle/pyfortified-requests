#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging

from pprintpp import pprint
from pyfortified_requests import (
    RequestsFortifiedDownload,
)
from pyfortified_requests.support import (
    HEADER_CONTENT_TYPE_APP_JSON
)
from pyfortified_logging import (
    LoggingFormat,
    LoggingOutput
)

# http://api.population.io/#!/population/retrievePopulationTableAllCountries
URL_REST_POPULATIONS = \
    'http://api.population.io:80/1.0/population/2018/aged/63/'

request_download = RequestsFortifiedDownload(
    logger_level=logging.DEBUG,
    logger_output=LoggingOutput.FILE,
    logger_format=LoggingFormat.JSON,
)

request_download.logger.note(request_download.logger.getLevelName().lower())
request_download.logger.info("Start".upper())

result = \
    request_download.request(
        request_method='GET',
        request_url=URL_REST_POPULATIONS,
        request_params=None,
        request_retry=None,
        request_headers=HEADER_CONTENT_TYPE_APP_JSON,
        request_label="REST Population"
    )

request_download.logger.info("Completed".upper(), extra=vars(result))

pprint("Logger file path: %s" % request_download.logger.logger_path)

logger_fp = open(request_download.logger.logger_path, 'r')
pprint(logger_fp.readlines())

pprint(request_download.logger.getLevelName())

json_rest_countries = result.json()
pprint(json_rest_countries)
