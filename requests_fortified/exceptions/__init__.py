#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @namespace requests_fortified

from .base import RequestsFortifiedBaseError

from .custom import (
    RequestsFortifiedError,
    RequestsFortifiedClientError,
    RequestsFortifiedServiceError,
    RequestsFortifiedModuleError,
    RequestsFortifiedValueError,
    RequestsFortifiedAuthenticationError,
)
