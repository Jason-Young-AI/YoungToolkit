#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) Jason Young (杨郑鑫).
#
# E-Mail: <AI.Jason.Young@outlook.com>
# 2020-10-30 15:16
#
# This source code is licensed under the WTFPL license found in the
# LICENSE file in the root directory of this source tree.


import re
import sys
import unicodedata

from yoolkit.constant import Constant

from chardet.universaldetector import UniversalDetector


constant = Constant()

# Wide(W) Narrow(Na) FullWidth(F) HalfWidth(H) Non East-Asian Width(N)
# The 'F' char must have a corresponding 'Na' char.
# The 'H' char must have a corresponding 'W' char.
# But 'Na' or 'W' not certainly.
# So 'F' can be easily converted to 'Na' by NFKC Normalization.
# 'W' may be still 'W' or converted to 'H'.
# Where Han chars like '国' is 'W' char, but it do not have a corresponding 'H' char. However, some char like '【', '「' need to be converted to '[' and '"' when processing western languages which can not converted by NFKC Normalization.
# See http://unicode.org/reports/tr11/ ; https://en.wikipedia.org/wiki/Unicode_equivalence for details.
constant.SPECIAL_TO_NORMAL = {
    r'([„“”《》「」«»])': '"',
    r'([‚`‘’])': '\'',
    r'([━–])' : '-',
    r'([。])': '.',
    r'([、])': ',',
    r'([〈])': '<',
    r'([〉])': '>',
    r'([【])': '[',
    r'([】])': ']',
    r'([∶])' : ':',
}

# Control, format, surrogate ... char are all divided into several categories. See http://www.unicode.org/reports/tr44/#PropertyValueAliases.txt for details.
constant.UNICODE_CHAR_CATEGORIES = {
    'L', 'Lu', 'Ll', 'Lt', 'LC', 'Lm', 'Lo',
    'M', 'Mn', 'Mc', 'Me',
    'N', 'Nd', 'Nl', 'No',
    'P', 'Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po',
    'S', 'Sm', 'Sc', 'Sk', 'So',
    'Z', 'Zs', 'Zl', 'Zp',
    'C', 'Cc', 'Cf', 'Cs', 'Co', 'Cn',
}


def detect_file_encoding(file_path, detect_times=50000):
    detector = UniversalDetector()
    time = 0
    with open(file_path, 'rb') as file:
        detector.reset()
        for line in file:
            time += 1
            if time > detect_times:
                break
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        file_encoding_type = detector.result['encoding']
        if file_encoding_type == 'GB2312' or file_encoding_type == 'GB18030':
            file_encoding_type = 'GBK'
        if file_encoding_type == 'Windows-1254':
            file_encoding_type = 'utf-8'
    return file_encoding_type


def unicode_category(char):
    return unicodedata.category(char)


def unicode_chars_by_category(string, category):
    chars = set()
    for char in string:
        if category in unicode_category(char):
            chars.add(char)
    return chars


def normalize(string, form='NFKC'):
    # For more information about 'NF*', please refer to Unicode equivalence(https://en.wikipedia.org/wiki/Unicode_equivalence)
    assert form in {'NFC', 'NFKC', 'NFD', 'NFKD'}, f'Do not support this kind of form: \'{form}\'!'
    string = unicodedata.normalize(form, string)
    for special_char, normal_char in constant.SPECIAL_TO_NORMAL.items():
        string = re.sub(special_char, normal_char, string)
    return ' '.join(string.split())
