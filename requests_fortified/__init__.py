#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @namespace requests_fortified

__title__ = 'requests-fortified'
__version__ = '0.1.0'
__version_info__ = tuple(__version__.split('.'))

__python_required_version__ = (3, 0)

from requests_fortified.support.requests_session_client import (RequestsSessionClient)

from .requests_fortified import (RequestsFortified)
from .requests_fortified_download import (RequestsFortifiedDownload)
from .requests_fortified_upload import (RequestsFortifiedUpload)
from .errors import RequestsFortifiedErrorCodes as HttpStatusCode
