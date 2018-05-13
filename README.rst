.. -*- mode: rst -*-

pyfortified-requests
------------------------

**Work In Progress**

Extension of Python HTTP `requests <https://pypi.python.org/pypi/requests>`_ with verbose
logging using `logging-fortified <https://pypi.python.org/pypi/logging-fortified>`_, and robust handling for
Downloading files containing JSON, CSV, and XML data formats and Streaming.

Important Note
^^^^^^^^^^^^^^

This Python project is a refactoring of `requests-mv-integration <https://pypi.org/project/requests-mv-integrations/>`_
for the purpose of general usage intent.

Work In Progress
^^^^^^^^^^^^^^^^

The following still needs to be performed for this Python project:

- Unit-testing: This project will be switching over to using Python native Unit testing framework `unittest <https://docs.python.org/3/library/unittest.html>`_.
- More concise documentation is required.
- Travis CI
- Badges


Badges
------

.. start-badges

.. list-table::
    :stub-columns: 1

    * - info
      - |license|
    * - package
      - |version| |supported-versions|


.. |license| image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :alt: License Status
    :target: https://opensource.org/licenses/MIT

.. |version| image:: https://img.shields.io/pypi/v/requests_fortified.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/requests_fortified

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/requests-fortified.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/requests-fortified

.. end-badges


Install
-------

.. code-block:: bash

    pip install requests_fortified


Architecture
------------

``requests-fortified`` is an extension of the `Python package requests <https://pypi.python.org/pypi/requests>`_
and it is used for handling all HTTP requests including APIs in REST and SOAP,
screen scrapping, and handling response downloads in JSON, XML, and CSV.

Usage
-----

.. code-block:: python

    URL_REST_COUNTRIES = \
        'https://restcountries.eu/rest/v2/all'

    from requests_fortified import (
        RequestsFortifiedDownload,
    )
    request_download = RequestsFortifiedDownload(logger_level=logging.DEBUG)

    result = \
        request_download.request(
            request_method='GET',
            request_url=URL_REST_COUNTRIES,
            request_params=None,
            request_retry=None,
            request_headers=HEADER_CONTENT_TYPE_APP_JSON,
            request_label="REST Countries"
        )

    json_rest_countries = result.json()

    pprint(json_rest_countries)


Example
^^^^^^^

.. code-block:: bash

    $ python3 examples/example_request.py

    ======================================================
    run-examples requests-fortified
    ======================================================
    rm -fR _tmp/*.json
    ======================================================
    'Logger file path: ./tmp/log_1526043820.json'
    [
        '{"asctime": "2018-05-11 06:03:26 -0700", "levelname": "NOTE", "name": "requests_fortified", "version": "0.1.0", "message": "debug"}\n',
        '{"asctime": "2018-05-11 06:03:26 -0700", "levelname": "INFO", "name": "requests_fortified", "version": "0.1.0", "message": "START"}\n',
        '{"asctime": "2018-05-11 06:03:26 -0700", "levelname": "DEBUG", "name": "requests_fortified", "version": "0.1.0", "message": "REST Countries: Start"}\n',
        '{"asctime": "2018-05-11 06:03:26 -0700", "levelname": "DEBUG", "name": "requests_fortified", "version": "0.1.0", "message": "REST Countries: Start: Details", "Disk:": {"path": "/", "total": "232.62 GB", "used": "134.44 GB", "free": "97.94 GB", "percent": 57}, "Mem": {"total": "16.00 GB", "used": "12.50 GB", "free": "147.59 KB", "shared": "0 B", "buffers": "0 B", "cached": "0 B"}, "allow_redirects": true, "build_request_curl": true, "cookie_payload": null, "request_auth": null, "request_cert": null, "request_data": null, "request_headers": {"Content-Type": "application/json", "User-Agent": "(requests-fortified/0.1.0, Python/3.6.5)"}, "request_json": null, "request_label": "REST Countries", "request_method": "GET", "request_params": null, "request_retry": {"timeout": 60, "tries": 3, "delay": 10}, "request_url": "https://restcountries.eu/rest/v2/all", "stream": false, "timeout": null, "verify": true}\n',
        '{"asctime": "2018-05-11 06:03:26 -0700", "levelname": "DEBUG", "name": "requests_fortified", "version": "0.1.0", "message": "REST Countries: Start", "request_label": "REST Countries", "request_retry_excps": ["ConnectTimeout", "ReadTimeout", "Timeout"], "request_retry_http_status_codes": [500, 502, 503, 504, 429], "timeout": null}\n',
        '{"asctime": "2018-05-11 06:03:26 -0700", "levelname": "DEBUG", "name": "requests_fortified", "version": "0.1.0", "message": "REST Countries: Attempt", "attempts": 1, "delay": 10, "request_label": "REST Countries", "request_url": "https://restcountries.eu/rest/v2/all", "timeout": 60, "tries": 3}\n',
        '{"asctime": "2018-05-11 06:03:26 -0700", "levelname": "DEBUG", "name": "requests_fortified", "version": "0.1.0", "message": "REST Countries: Session: Details", "cookie_payload": {}, "request_label": "REST Countries"}\n',
        '{"asctime": "2018-05-11 06:03:26 -0700", "levelname": "DEBUG", "name": "requests_fortified", "version": "0.1.0", "message": "REST Countries: Details", "request_data": "", "request_headers": {"Content-Type": "application/json", "User-Agent": "(requests-fortified/0.1.0, Python/3.6.5)"}, "request_label": "REST Countries", "request_method": "GET", "request_params": {}, "request_url": "https://restcountries.eu/rest/v2/all", "timeout": 60}\n',
        '{"asctime": "2018-05-11 06:03:26 -0700", "levelname": "NOTE", "name": "requests_fortified", "version": "0.1.0", "message": "REST Countries: Curl", "request_curl": "curl --verbose -X GET -H \'Content-Type: application/json\' -H \'User-Agent: (requests-fortified/0.1.0, Python/3.6.5)\' --connect-timeout 60 -L \'https://restcountries.eu/rest/v2/all\'", "request_label": "REST Countries", "request_method": "GET"}\n',
        '{"asctime": "2018-05-11 06:03:26 -0700", "levelname": "DEBUG", "name": "requests_fortified.support.requests_session_client", "version": "0.1.0", "message": "Session Request: Details", "allow_redirects": true, "headers": {"Content-Type": "application/json", "User-Agent": "(requests-fortified/0.1.0, Python/3.6.5)"}, "method": "GET", "timeout": 60, "url": "https://restcountries.eu/rest/v2/all", "verify": true}\n',
        '{"asctime": "2018-05-11 06:03:27 -0700", "levelname": "DEBUG", "name": "requests_fortified", "version": "0.1.0", "message": "REST Countries: Response: Details", "http_status_code": 200, "http_status_desc": "Request fulfilled, document follows", "http_status_type": "Successful", "response_headers": {"Date": "Fri, 11 May 2018 13:03:27 GMT", "Content-Type": "application/json;charset=utf-8", "Transfer-Encoding": "chunked", "Connection": "keep-alive", "Set-Cookie": "__cfduid=d46030914d4b01044c167b67bbca43b951526043807; expires=Sat, 11-May-19 13:03:27 GMT; path=/; domain=.restcountries.eu; HttpOnly", "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET", "Access-Control-Allow-Headers": "Accept, X-Requested-With", "Cache-Control": "public, max-age=86400", "Expect-CT": "max-age=604800, report-uri=\\"https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct\\"", "Server": "cloudflare", "CF-RAY": "4194d881fc146bd4-SJC", "Content-Encoding": "gzip"}}\n',
        '{"asctime": "2018-05-11 06:03:27 -0700", "levelname": "DEBUG", "name": "requests_fortified", "version": "0.1.0", "message": "REST Countries: Cookie Payload", "cookie_payload": {"__cfduid": "d46030914d4b01044c167b67bbca43b951526043807"}, "request_label": "REST Countries"}\n',
        '{"asctime": "2018-05-11 06:03:27 -0700", "levelname": "DEBUG", "name": "requests_fortified", "version": "0.1.0", "message": "REST Countries: Try Send Request: Is Return Response: Checking", "request_url": "https://restcountries.eu/rest/v2/all"}\n',
        '{"asctime": "2018-05-11 06:03:27 -0700", "levelname": "DEBUG", "name": "requests_fortified", "version": "0.1.0", "message": "REST Countries: Try Send Request: Is Return Response: Valid", "request_url": "https://restcountries.eu/rest/v2/all"}\n',
        '{"asctime": "2018-05-11 06:03:27 -0700", "levelname": "INFO", "name": "requests_fortified", "version": "0.1.0", "message": "REST Countries: Finished", "request_time_msecs": 569}\n',
        '{"asctime": "2018-05-11 06:03:27 -0700", "levelname": "DEBUG", "name": "requests_fortified", "version": "0.1.0", "message": "REST Countries: Usage", "Disk:": {"path": "/", "total": "232.62 GB", "used": "134.44 GB", "free": "97.94 GB", "percent": 57}, "Mem": {"total": "16.00 GB", "used": "12.50 GB", "free": "145.89 KB", "shared": "0 B", "buffers": "0 B", "cached": "0 B"}}\n',
        '{"asctime": "2018-05-11 06:03:27 -0700", "levelname": "INFO", "name": "requests_fortified", "version": "0.1.0", "message": "COMPLETED", "connection": "<requests.adapters.HTTPAdapter object at 0x1043b11d0>", "cookies": "<RequestsCookieJar[<Cookie __cfduid=d46030914d4b01044c167b67bbca43b951526043807 for .restcountries.eu/>]>", "elapsed": "0:00:00.286022", "encoding": "utf-8", "headers": "{\'Date\': \'Fri, 11 May 2018 13:03:27 GMT\', \'Content-Type\': \'application/json;charset=utf-8\', \'Transfer-Encoding\': \'chunked\', \'Connection\': \'keep-alive\', \'Set-Cookie\': \'__cfduid=d46030914d4b01044c167b67bbca43b951526043807; expires=Sat, 11-May-19 13:03:27 GMT; path=/; domain=.restcountries.eu; HttpOnly\', \'Access-Control-Allow-Origin\': \'*\', \'Access-Control-Allow-Methods\': \'GET\', \'Access-Control-Allow-Headers\': \'Accept, X-Requested-With\', \'Cache-Control\': \'public, max-age=86400\', \'Expect-CT\': \'max-age=604800, report-uri=\\"https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct\\"\', \'Server\': \'cloudflare\', \'CF-RAY\': \'4194d881fc146bd4-SJC\', \'Content-Encoding\': \'gzip\'}", "history": [], "raw": "<urllib3.response.HTTPResponse object at 0x1043b1dd8>", "reason": "", "request": "<PreparedRequest [GET]>", "status_code": 200, "url": "https://restcountries.eu/rest/v2/all"}\n',
    ]
    'DEBUG'
    [
        {
            'alpha2Code': 'AF',
            'alpha3Code': 'AFG',
            'altSpellings': ['AF', 'Afġānistān'],
            'area': 652230.0,
            'borders': ['IRN', 'PAK', 'TKM', 'UZB', 'TJK', 'CHN'],
            'callingCodes': ['93'],
            'capital': 'Kabul',
            'cioc': 'AFG',
            'currencies': [
                {'code': 'AFN', 'name': 'Afghan afghani', 'symbol': '؋'},
            ],
            'demonym': 'Afghan',
            'flag': 'https://restcountries.eu/data/afg.svg',
            'gini': 27.8,
            'languages': [
                {
                    'iso639_1': 'ps',
                    'iso639_2': 'pus',
                    'name': 'Pashto',
                    'nativeName': 'پښتو',
                },
                {
                    'iso639_1': 'uz',
                    'iso639_2': 'uzb',
                    'name': 'Uzbek',
                    'nativeName': 'O\u02bbzbek',
                },
                {
                    'iso639_1': 'tk',
                    'iso639_2': 'tuk',
                    'name': 'Turkmen',
                    'nativeName': 'Türkmen',
                },
            ],
            'latlng': [33.0, 65.0],
            'name': 'Afghanistan',
            'nativeName': 'افغانستان',
            'numericCode': '004',
            'population': 27657145,
            'region': 'Asia',
            'regionalBlocs': [
                {
                    'acronym': 'SAARC',
                    'name': 'South Asian Association for Regional Cooperation',
                    'otherAcronyms': [],
                    'otherNames': [],
                },
            ],
            'subregion': 'Southern Asia',
            'timezones': ['UTC+04:30'],
            'topLevelDomain': ['.af'],
            'translations': {
                'br': 'Afeganistão',
                'de': 'Afghanistan',
                'es': 'Afganistán',
                'fa': 'افغانستان',
                'fr': 'Afghanistan',
                'hr': 'Afganistan',
                'it': 'Afghanistan',
                'ja': 'アフガニスタン',
                'nl': 'Afghanistan',
                'pt': 'Afeganistão',
            },
        },


Classes
-------

- ``class RequestsFortified`` -- Base class using `requests <https://pypi.python.org/pypi/requests>`_ with retry functionality and verbose logging.
- ``class RequestsFortifiedDownload`` -- Download file handling.
- ``class RequestsFortifiedUpload`` -- Upload file handling.

Requirements
------------

``requests-fortified`` module is built upon Python 3 and has dependencies upon
several Python modules available within `Python Package Index PyPI <https://pypi.python.org/pypi>`_.

.. code-block:: bash

    make install

or

.. code-block:: bash

    python3 -m pip uninstall --yes --no-input -r requirements.txt
    python3 -m pip install --upgrade -r requirements.txt


Packages
^^^^^^^^

- **beautifulsoup4**: https://pypi.python.org/pypi/beautifulsoup4
- **deepdiff**: https://pypi.python.org/pypi/deepdiff
- **logging-fortified**: ***TBD***
- **pyhttpstatus-utils**: https://pypi.python.org/pypi/pyhttpstatus-utils
- **requests**: https://pypi.python.org/pypi/requests
- **safe-cast**: https://pypi.python.org/pypi/safe-cast
