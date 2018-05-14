#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @namespace pyfortified_requests

import json
import time


class Metrics(object):
    '''
    A container class for metrics.
    Intended to be used by RequestsFortified to capture api requests metrics.
    '''
    _metrics_dict = {}

    def inc(self, name, delta=1):
        """
        Increment counter <name>
        :param name: name of counter
        :param delta: the amount to increment
        :return: None
        """
        value = self._metrics_dict.setdefault(name, 0)
        self._metrics_dict[name] = value + delta

    def set(self, name, value):
        """
        Set gauge <name>
        :param name: name of gauge
        :param value: the value to set
        :return: None
        """
        self._metrics_dict[name] = value

    def add_sample(self, name, value):
        """
        Add a <value> sample to metric <name>
        :param name: name of metric
        :param value: the sample value to add
        :return: None
        """
        # Samples for metric <name> are kept in a list, as (time, value) pairs.
        samples = self._metrics_dict.setdefault(name, list())
        samples.append((time.time(), value))

    def dict(self):
        return self._metrics_dict

    def json(self):
        return str(json.dumps(self._metrics_dict))
