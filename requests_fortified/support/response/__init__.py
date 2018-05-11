#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @namespace requests_fortified

from .csv import (
    csv_skip_last_row,
)
from .parse import (
    requests_response_text_html,
    requests_response_text_xml,
)
from .validate import (
    build_response_error_details,
    handle_json_decode_error,
    requests_response_json,
    validate_json_response,
    validate_response,
)
