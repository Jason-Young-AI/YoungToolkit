#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) Jason Young (杨郑鑫).
#
# E-Mail: <AI.Jason.Young@outlook.com>
# 2020-11-01 12:33
#
# This source code is licensed under the WTFPL license found in the
# LICENSE file in the root directory of this source tree.


import re


def encode(string):
    string = re.sub(r'\&amp;amp;', '&', string)
    string = re.sub(r'\&amp;', '&', string)
    string = re.sub(r'\&quot', '"', string)
    string = re.sub(r'\&apos', "'", string)
    string = re.sub(r'\&lt', '<', string)
    string = re.sub(r'\&gt', '>', string)

    string = re.sub(r'\&bar;', '|', string)
    string = re.sub(r'\&#124', '|', string)

    string = re.sub(r'\&bra;', '[', string)
    string = re.sub(r'\&#91;', '[', string)

    string = re.sub(r'\&ket;', ']', string)
    string = re.sub(r'\&#93;', ']', string)

    return string

def decode(string):
    string = re.sub(r'\&', '&amp;', string)
    string = re.sub(r'\"', '&quot;', string)
    string = re.sub(r'\'', '&apos;', string)
    string = re.sub(r'\<', '&lt;', string)
    string = re.sub(r'\>', '&gt;', string)

    string = re.sub(r'\|', '&bar;', string)
    string = re.sub(r'\[', '&bra;', string)
    string = re.sub(r'\]', '&ket;', string)

    return string
