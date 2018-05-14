#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @namespace pyfortified_requests

import sys
import traceback


def get_exception_message(ex):
    """Build exception message with details.
    """
    template = "{0}: {1!r}"
    return template.format(type(ex).__name__, ex.args)


def print_traceback(ex):
    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_tb)


def print_limited_traceback(ex, limit=1):
    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback.print_exc(limit=1, file=sys.stdout)


def print_traceback_stack():
    """Provide traceback of provided exception.
    """
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))

    exception_str = "Traceback (most recent call last):\n"
    exception_str += "".join(exception_list)
    # Removing the last \n
    exception_str = exception_str[:-1]

    print(exception_str)
