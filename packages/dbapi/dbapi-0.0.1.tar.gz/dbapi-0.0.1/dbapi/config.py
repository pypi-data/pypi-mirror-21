#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2017 The Authors. All Rights Reserved.
# License: MIT.
# Author: acrazing <joking.young@gmail.com>.
# File: config.
import logging

import sys

api_config = {
    'persist_file': '__cache__.dat',
    'headers': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh,zh-CN;q=0.8,zh-TW;q=0.6,en;q=0.4,en-US;q=0.2',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 '
                      'Safari/537.36',
    },
    'logger': 'dbapi',
    'log_level': logging.DEBUG,
    'log_destination': sys.stderr,
}
