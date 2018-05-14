.. -*- mode: rst -*-

pyfortified-requests
--------------------

Extension of Python HTTP `requests <https://pypi.python.org/pypi/requests>`_ with verbose
logging using `pyfortified-logging <https://pypi.org/project/pyfortified-logging>`_, and robust handling for
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


Install
-------

.. code-block:: bash

    pip install pyfortified_requests


Architecture
------------

``pyfortified-requests`` is an extension of the `Python package requests <https://pypi.python.org/pypi/requests>`_
and it is used for handling all HTTP requests including APIs in REST and SOAP,
screen scrapping, and handling response downloads in JSON, XML, and CSV.

Usage
-----

.. code-block:: python

    URL_REST_COUNTRIES = \
        'http://api.population.io/1.0/countries'

    from pyfortified_requests import (
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

    $ make run-example-countries

    ======================================================
    run-examples pyfortified-requests
    ======================================================
    rm -fR _tmp/*.json
    ======================================================
    'Logger file path: ./tmp/log_1526043820.json'
    [
        '{"asctime": "2018-05-14 10:40:54 -0700", "levelname": "NOTE", "name": "pyfortified_requests", "version": "0.3.3", "message": "debug"}\n',
        '{"asctime": "2018-05-14 10:40:55 -0700", "levelname": "INFO", "name": "pyfortified_requests", "version": "0.3.3", "message": "START"}\n',
        '{"asctime": "2018-05-14 10:40:55 -0700", "levelname": "DEBUG", "name": "pyfortified_requests", "version": "0.3.3", "message": "REST Countries: Start"}\n',
        '{"asctime": "2018-05-14 10:40:55 -0700", "levelname": "DEBUG", "name": "pyfortified_requests", "version": "0.3.3", "message": "REST Countries: Start: Details", "Disk:": {"free": "91.54 GB", "percent": 60, "total": "232.62 GB", "path": "/", "used": "140.84 GB"}, "Mem": {"free": "133.81 KB", "cached": "0 B", "total": "16.00 GB", "used": "13.19 GB", "shared": "0 B", "buffers": "0 B"}, "allow_redirects": true, "build_request_curl": true, "cookie_payload": null, "request_auth": null, "request_cert": null, "request_data": null, "request_headers": {"Content-Type": "application/json", "User-Agent": "(pyfortified-requests/0.3.3, Python/3.5.4)"}, "request_json": null, "request_label": "REST Countries", "request_method": "GET", "request_params": null, "request_retry": {"tries": 3, "delay": 10, "timeout": 60}, "request_url": "http://api.population.io/1.0/countries", "stream": false, "timeout": null, "verify": true}\n',
        '{"asctime": "2018-05-14 10:40:55 -0700", "levelname": "DEBUG", "name": "pyfortified_requests", "version": "0.3.3", "message": "REST Countries: Start", "request_label": "REST Countries", "request_retry_excps": ["ConnectTimeout", "ReadTimeout", "Timeout"], "request_retry_http_status_codes": [500, 502, 503, 504, 429], "timeout": null}\n',
        '{"asctime": "2018-05-14 10:40:55 -0700", "levelname": "DEBUG", "name": "pyfortified_requests", "version": "0.3.3", "message": "REST Countries: Attempt", "attempts": 1, "delay": 10, "request_label": "REST Countries", "request_url": "http://api.population.io/1.0/countries", "timeout": 60, "tries": 3}\n',
        '{"asctime": "2018-05-14 10:40:55 -0700", "levelname": "DEBUG", "name": "pyfortified_requests", "version": "0.3.3", "message": "REST Countries: Session: Details", "cookie_payload": {}, "request_label": "REST Countries"}\n',
        '{"asctime": "2018-05-14 10:40:55 -0700", "levelname": "DEBUG", "name": "pyfortified_requests", "version": "0.3.3", "message": "REST Countries: Details", "request_data": "", "request_headers": {"Content-Type": "application/json", "User-Agent": "(pyfortified-requests/0.3.3, Python/3.5.4)"}, "request_label": "REST Countries", "request_method": "GET", "request_params": {}, "request_url": "http://api.population.io/1.0/countries", "timeout": 60}\n',
        '{"asctime": "2018-05-14 10:40:55 -0700", "levelname": "NOTE", "name": "pyfortified_requests", "version": "0.3.3", "message": "REST Countries: Curl", "request_curl": "curl --verbose -X GET -H \'Content-Type: application/json\' -H \'User-Agent: (pyfortified-requests/0.3.3, Python/3.5.4)\' --connect-timeout 60 -L \'http://api.population.io/1.0/countries\'", "request_label": "REST Countries", "request_method": "GET"}\n',
        '{"asctime": "2018-05-14 10:40:55 -0700", "levelname": "DEBUG", "name": "pyfortified_requests.support.requests_session_client", "version": "0.3.3", "message": "Session Request: Details", "allow_redirects": true, "headers": {"Content-Type": "application/json", "User-Agent": "(pyfortified-requests/0.3.3, Python/3.5.4)"}, "method": "GET", "timeout": 60, "url": "http://api.population.io/1.0/countries", "verify": true}\n',
        '{"asctime": "2018-05-14 10:40:55 -0700", "levelname": "DEBUG", "name": "pyfortified_requests", "version": "0.3.3", "message": "REST Countries: Response: Details", "http_status_code": 200, "http_status_desc": "Request fulfilled, document follows", "http_status_type": "Successful", "response_headers": {"Vary": "Accept", "Allow": "OPTIONS, GET", "Cache-Control": "max-age=3600", "Via": "1.1 7bfcc2251021d9dc94a87ff179d69731.cloudfront.net (CloudFront)", "Expires": "Mon, 14 May 2018 18:23:07 GMT", "Connection": "keep-alive", "X-Amz-Cf-Id": "_Q_sioBJ9zkP0pFZztqnQJHLBXl5DWoAnGnb2HBGxJHDEmPX4jH82g==", "Date": "Mon, 14 May 2018 17:23:07 GMT", "Content-Type": "application/json", "Server": "nginx/1.10.2", "Content-Length": "1572", "X-Cache": "Hit from cloudfront", "Age": "1039", "Content-Encoding": "gzip"}}\n',
        '{"asctime": "2018-05-14 10:40:55 -0700", "levelname": "DEBUG", "name": "pyfortified_requests", "version": "0.3.3", "message": "REST Countries: Cookie Payload", "cookie_payload": {}, "request_label": "REST Countries"}\n',
        '{"asctime": "2018-05-14 10:40:55 -0700", "levelname": "DEBUG", "name": "pyfortified_requests", "version": "0.3.3", "message": "REST Countries: Try Send Request: Is Return Response: Checking", "request_url": "http://api.population.io/1.0/countries"}\n',
        '{"asctime": "2018-05-14 10:40:55 -0700", "levelname": "DEBUG", "name": "pyfortified_requests", "version": "0.3.3", "message": "REST Countries: Try Send Request: Is Return Response: Valid", "request_url": "http://api.population.io/1.0/countries"}\n',
        '{"asctime": "2018-05-14 10:40:55 -0700", "levelname": "INFO", "name": "pyfortified_requests", "version": "0.3.3", "message": "REST Countries: Finished", "request_time_msecs": 96}\n',
        '{"asctime": "2018-05-14 10:40:55 -0700", "levelname": "DEBUG", "name": "pyfortified_requests", "version": "0.3.3", "message": "REST Countries: Usage", "Disk:": {"free": "91.54 GB", "percent": 60, "total": "232.62 GB", "path": "/", "used": "140.84 GB"}, "Mem": {"free": "133.17 KB", "cached": "0 B", "total": "16.00 GB", "used": "13.19 GB", "shared": "0 B", "buffers": "0 B"}}\n',
        '{"asctime": "2018-05-14 10:40:55 -0700", "levelname": "INFO", "name": "pyfortified_requests", "version": "0.3.3", "message": "COMPLETED", "connection": "<requests.adapters.HTTPAdapter object at 0x104096be0>", "cookies": "<RequestsCookieJar[]>", "elapsed": "0:00:00.079948", "encoding": null, "headers": "{\'Allow\': \'OPTIONS, GET\', \'Cache-Control\': \'max-age=3600\', \'Content-Length\': \'1572\', \'Vary\': \'Accept\', \'Age\': \'1039\', \'Connection\': \'keep-alive\', \'X-Cache\': \'Hit from cloudfront\', \'Content-Type\': \'application/json\', \'Server\': \'nginx/1.10.2\', \'Via\': \'1.1 7bfcc2251021d9dc94a87ff179d69731.cloudfront.net (CloudFront)\', \'Expires\': \'Mon, 14 May 2018 18:23:07 GMT\', \'Date\': \'Mon, 14 May 2018 17:23:07 GMT\', \'X-Amz-Cf-Id\': \'_Q_sioBJ9zkP0pFZztqnQJHLBXl5DWoAnGnb2HBGxJHDEmPX4jH82g==\', \'Content-Encoding\': \'gzip\'}", "history": [], "raw": "<urllib3.response.HTTPResponse object at 0x1040a86d8>", "reason": "OK", "request": "<PreparedRequest [GET]>", "status_code": 200, "url": "http://api.population.io/1.0/countries"}\n',
    ]
    'DEBUG'
    {
        'countries': [
            'Afghanistan',
            'AFRICA',
            'Albania',
            'Algeria',
            'Angola',
            'Antigua and Barbuda',
            'Arab Rep of Egypt',
            'Argentina',
            'Armenia',
            'Aruba',
            'ASIA',
            'Australia',
            'Australia/New Zealand',
            'Austria',
            'Azerbaijan',
            'The Bahamas',
            ***
            'Uganda',
            'Ukraine',
            'United Arab Emirates',
            'United Kingdom',
            'United States',
            'US Virgin Islands',
            'Uruguay',
            'Uzbekistan',
            'Vanuatu',
            'Vietnam',
            'Western Africa',
            'Western Asia',
            'Western Europe',
            'Western Sahara',
            'World',
            'Zambia',
            'Zimbabwe',
        ],
    }

Classes
-------

- ``class RequestsFortified`` -- Base class using `requests <https://pypi.python.org/pypi/requests>`_ with retry functionality and verbose logging.
- ``class RequestsFortifiedDownload`` -- Download file handling.
- ``class RequestsFortifiedUpload`` -- Upload file handling.

Requirements
------------

``pyfortified-requests`` module is built upon Python 3 and has dependencies upon
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
- **pyfortified-logging**: https://pypi.org/project/pyfortified-logging
- **pyhttpstatus-utils**: https://pypi.python.org/pypi/pyhttpstatus-utils
- **requests**: https://pypi.python.org/pypi/requests
- **safe-cast**: https://pypi.python.org/pypi/safe-cast
