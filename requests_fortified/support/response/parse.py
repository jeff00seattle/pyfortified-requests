#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @namespace requests_fortified

import logging
import ujson as json
import xmltodict
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)

# from pprintpp import pprint


def requests_response_text_html(response):
    """Get HTML Text only

    Args:
        response:

    Returns:

    """
    assert response

    response_content_html_lines = None
    response_content_type = response.headers.get('Content-Type', None)

    if response_content_type.startswith('text/html'):
        try:
            response_content_html = response.text
            soup = BeautifulSoup(response_content_html, 'html.parser')
            for elem in soup.findAll(['script', 'style']):
                elem.extract()
            response_content_html_text = soup.get_text()
            response_content_html_lines = response_content_html_text.splitlines()
            response_content_html_lines = \
                [item.strip() for item in response_content_html_lines]
            response_content_html_lines = \
                [x for x in response_content_html_lines if x != '']
        except Exception as ex:
            raise ValueError("Failed to parse text/html", errors=ex)
    else:
        raise ValueError("Unexpected 'Content-Type': '{0}'".format(response_content_type))

    return response_content_html_lines


def requests_response_text_xml(response):
    """Get HTML Text only

    Args:
        response:

    Returns:

    """
    assert response

    response_http_status_code = response.status_code
    response_content_type = response.headers.get('Content-Type', None)

    response_content = response.text
    response_content_length = len(response_content)

    xml_json = None
    if response_content_type.startswith('text/xml') \
            or response_content_type.startswith('application/xml'):
        if response_http_status_code == 200 and \
                response_content_length > 0 and \
                response_content:
            xml_dictionary = xmltodict.parse(response_content)
            xml_json = json.loads(json.dumps(xml_dictionary))

    else:
        raise ValueError("Unexpected 'Content-Type': '{0}'".format(response_content_type))

    return xml_json
