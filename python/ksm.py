#!/usr/bin/env python

# Copyright (C) 2015 Bernd Zeimetz <bernd@bzed.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
# Authors:
#   Bernd Zeimetz <bernd@bzed.de>

if __name__ != '__main__':
    import collectd

import os
import sys
import time

PLUGIN_NAME='ksm'
SYSFS_PATH = '/sys/kernel/mm/ksm'
DEBUG=False

COLLECTD_DATA = [
    ('vmpage_number',    'shared',   'pages_shared'),
    ('vmpage_number',    'saved',    'pages_sharing'),
    ('vmpage_number',    'unshared', 'pages_unshared'),
    ('vmpage_number',    'volatile', 'pages_volatile'),
    ('total_operations', 'scan',     'full_scans'),
]

def read_sysfs_file(filename):
    with open(os.path.join(SYSFS_PATH, filename), 'r') as fd:
        return fd.read().strip()

def collectd_dispatch(collectd_type, type_instance, value):
    val = collectd.Values(plugin=PLUGIN_NAME, type=collectd_type)
    val.type_instance = type_instance
    val.values = [ value ]
    val.dispatch()
dispatch = collectd_dispatch

def debug_dispatch(collectd_type, type_instance, value):
    print("DEBUG: %s/%s-%s = %s" %(PLUGIN_NAME, collectd_type, type_instance, value))

def read_callback():
    for collectd_type, type_instance, filename in COLLECTD_DATA:
        try:
            dispatch(collectd_type, type_instance, read_sysfs_file(filename))
        except Exception, e:
            if DEBUG:
                print(e)

if __name__ == '__main__':
    dispatch = debug_dispatch
    DEBUG=True
    read_callback()
else:
    collectd.register_read(read_callback)
