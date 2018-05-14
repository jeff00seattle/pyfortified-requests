#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @namespace pyfortified_requests

__title__ = 'pyfortified-requests'
__version__ = '0.3.4'
__version_info__ = tuple(__version__.split('.'))

__python_required_version__ = (3, 0)

from pyfortified_requests.support.requests_session_client import (RequestsSessionClient)

from .pyfortified_requests import (RequestsFortified)
from .pyfortified_requests_download import (RequestsFortifiedDownload)
from .pyfortified_requests_upload import (RequestsFortifiedUpload)
from .errors import RequestsFortifiedErrorCodes as HttpStatusCode
