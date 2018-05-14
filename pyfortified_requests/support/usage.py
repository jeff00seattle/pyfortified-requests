#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @namespace pyfortified_requests

import os
import psutil
from pyfortified_requests.support.utils import bytes_to_human
from pyfortified_requests.support.constants import IRONIO_PARTITION


def mem_usage():
    virt = psutil.virtual_memory()
    return {
        'Mem': {
            'total': bytes_to_human(virt.total),
            'used': bytes_to_human(virt.used),
            'free': bytes_to_human(virt.free / 1024),
            'shared': bytes_to_human(getattr(virt, 'shared', 0)),
            'buffers': bytes_to_human(getattr(virt, 'buffers', 0)),
            'cached': bytes_to_human(getattr(virt, 'cached', 0))
        },
    }


def disk_usage(dir=None):
    if dir is None:
        dir = IRONIO_PARTITION

    if not os.path.exists(dir):
        dir = '/'

    usage = psutil.disk_usage(dir)
    return {
        'Disk:': {
            'path': dir,
            'total': bytes_to_human(usage.total),
            'used': bytes_to_human(usage.used),
            'free': bytes_to_human(usage.free),
            'percent': int(usage.percent)
        }
    }


def env_usage(dir=None):
    usage = {}
    usage.update(disk_usage(dir))
    usage.update(mem_usage())
    return usage
