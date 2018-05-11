#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @namespace requests_fortified

import six
from requests_fortified import (__title__)
from requests_fortified.errors import (RequestsFortifiedErrorCodes)
from requests_fortified.errors import error_desc as requests_fortified_error_desc
from requests_fortified.errors import error_name as requests_fortified_error_name
from safe_cast import safe_str

# from pprintpp import pprint


# @brief Requests Fortified Base Exception
#
# @namespace requests_fortified.RequestsFortifiedBaseError
class RequestsFortifiedBaseError(Exception):
    """Requests Fortified Base Exception
    """
    __error_message = None
    __errors = None
    __error_code = None
    __error_status = None
    __error_reason = None
    __error_details = None
    __error_origin = None
    __error_request_curl = None

    def __init__(
        self,
        error_message=None,
        errors=None,
        error_code=None,
        error_status=None,
        error_reason=None,
        error_details=None,
        error_origin=None,
        error_request_curl=None
    ):
        self.__error_code = RequestsFortifiedErrorCodes.REQ_ERR_UNEXPECTED
        self.__error_origin = __title__

        if error_code is not None:
            self.__error_code = error_code

        if error_origin is not None:
            self.__error_origin = error_origin

        self.__error_message = RequestsFortifiedBaseError._error_message(
            error_message=error_message,
            error_code=self.__error_code,
        )

        # Call the base class constructor with the parameters it needs
        super(RequestsFortifiedBaseError, self).__init__(self.error_message)

        self.__errors = errors or None
        self.__error_status = error_status or None
        self.__error_reason = error_reason or None
        self.__error_details = error_details or None
        self.__error_request_curl = error_request_curl or None

    @property
    def error_message(self):
        """Get property of message object.
        """
        return self.__error_message

    @property
    def errors(self):
        """Get property of error object."""
        return self.__errors

    @property
    def error_code(self):
        """Get property of exit code.
        """
        return self.__error_code

    @property
    def error_reason(self):
        """Get property of response reason for error.
        """
        return self.__error_reason

    @property
    def error_status(self):
        """Get property of response status code.
        """
        return self.__error_status

    @property
    def error_details(self):
        """Get property of error details.
        """
        return self.__error_details

    @property
    def error_origin(self):
        """Get property of error origin.
        """
        return self.__error_origin

    @property
    def error_request_curl(self):
        """Get property of error request curl.
        """
        return self.__error_request_curl

    @error_request_curl.setter
    def error_request_curl(self, value):
        """Set property of error request curl.
        """
        self.__error_request_curl = value

    @staticmethod
    def _error_message(error_message, error_code):
        error_message_ = None
        exit_code_description_ = requests_fortified_error_desc(error_code).rstrip('\.')

        error_message_prefix_ = "{0}: {1}".format(error_code, exit_code_description_)

        error_message = safe_str(error_message).strip()

        if error_message:
            error_message_ = "%s: '%s'" % (error_message_prefix_, six.text_type(error_message))
        elif exit_code_description_:
            error_message_ = error_message_prefix_

        return error_message_

    def __str__(self):
        """Stringify
        """
        error_origin = self.error_origin
        error_message = self.error_message

        if not error_message or len(error_message) == 0:
            error_message = None

        if self.error_reason:
            if error_message:
                error_message += ", "
            else:
                error_message = ""
            error_message += "Error Reason: '{0}'".format(self.error_reason)
        if self.error_status:
            if error_message:
                error_message += ", "
            else:
                error_message = ""
            error_message += "Exit Status: {0}".format(self.error_status)
        if self.error_code:
            if error_message:
                error_message += ", "
            else:
                error_message = ""
            error_message += "Exit Code: {0}, Exit Name: {1}".format(self.error_code, requests_fortified_error_name(self.error_code))
        if self.error_details:
            if error_message:
                error_message += ", "
            else:
                error_message = ""
            error_message += "Error Details: {0}".format(self.error_details)
        if self.errors:
            if error_message:
                error_message += ", "
            else:
                error_message = ""
            error_message += "Errors: {0}".format(self.errors)

        return "{0}: {1}".format(error_origin, error_message)

    def to_dict(self):

        dict_ = {
            'error_origin': self.error_origin,
            'exit_code': self.error_code,
            'exit_desc': requests_fortified_error_desc(self.error_code),
            'exit_name': requests_fortified_error_name(self.error_code)
        }

        if self.error_message:
            dict_.update({'error_message': self.error_message})
        if self.error_status:
            dict_.update({'error_status': self.error_status})
        if self.error_reason:
            dict_.update({'error_reason': self.error_reason})
        if self.error_details:
            dict_.update({'error_details': self.error_details})
        if self.errors:
            dict_.update({'errors': self.errors})

        return dict_
