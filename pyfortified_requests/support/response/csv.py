#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @namespace pyfortified_requests


def csv_skip_last_row(iterator):
    """Skip last CSV row.

    Args:
        iterator:

    Returns:

    """
    prev = next(iterator)
    for item in iterator:
        yield prev
        prev = item
