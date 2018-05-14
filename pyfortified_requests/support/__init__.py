#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @namespace pyfortified_requests

from .bom_encoding import (
    detect_bom,
    get_bom_encoding,
    remove_bom,
)
from .constants import (
    HEADER_CONTENT_TYPE_APP_JSON,
    HEADER_CONTENT_TYPE_APP_URLENCODED,
    HEADER_USER_AGENT,
    IRONIO_PARTITION,
    REQUEST_RETRY_EXCPS,
    REQUEST_RETRY_HTTP_STATUS_CODES,
    __LOGGER_NAME__,
    __MODULE_SIG__,
    __PYTHON_VERSION__,
    __TIMEZONE_NAME_DEFAULT__,
    __USER_AGENT__,
)
from .curl import (
    command_line_request_curl,
    parse_curl,
)
from .response import (
    build_response_error_details,
    csv_skip_last_row,
    handle_json_decode_error,
    requests_response_json,
    requests_response_text_html,
    requests_response_text_xml,
    validate_json_response,
    validate_response,
)
from .retry_exception import mv_request_retry_excps_func
from .requests_session_client import RequestsSessionClient
from .utils import (
    base_class_name,
    bytes_to_human,
    full_class_name,
    python_check_version,
    urlencode_dict,
)
from .usage import (
    disk_usage,
    env_usage,
    mem_usage,
)
from .metrics import Metrics
