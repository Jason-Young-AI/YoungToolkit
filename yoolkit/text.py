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


def is_CJK_char(char):
    # The following is based on http://en.wikipedia.org/wiki/Basic_Multilingual_Plane#Basic_Multilingual_Plane
    # Hangul Jamo (1100–11FF)
    if ord(u'\U00001100') <= ord(char) and ord(char) <= ord(u'\U000011FF'):
        return True

    # CJK Radicals Supplement (2E80–2EFF)
    # Kangxi Radicals (2F00–2FDF)
    # Ideographic Description Characters (2FF0–2FFF)
    # CJK Symbols and Punctuation (3000–303F)
    # Hiragana (3040–309F)
    # Katakana (30A0–30FF)
    # Bopomofo (3100–312F)
    # Hangul Compatibility Jamo (3130–318F)
    # Kanbun (3190–319F)
    # Bopomofo Extended (31A0–31BF)
    # CJK Strokes (31C0–31EF)
    # Katakana Phonetic Extensions (31F0–31FF)
    # Enclosed CJK Letters and Months (3200–32FF)
    # CJK Compatibility (3300–33FF)
    # CJK Unified Ideographs Extension A (3400–4DBF)
    # Yijing Hexagram Symbols (4DC0–4DFF)
    # CJK Unified Ideographs (4E00–9FFF)
    # Yi Syllables (A000–A48F)
    # Yi Radicals (A490–A4CF)
    if ord(u'\U00002E80') <= ord(char) and ord(char) <= ord(u'\U0000A4CF'):
        return True

    # Phags-pa (A840–A87F)
    if ord(u'\U0000A840') <= ord(char) and ord(char) <= ord(u'\U0000A87F'):
        return True

    # Hangul Syllables (AC00–D7AF)
    if ord(u'\U0000AC00') <= ord(char) and ord(char) <= ord(u'\U0000D7AF'):
        return True

    # CJK Compatibility Ideographs (F900–FAFF)
    if ord(u'\U0000F900') <= ord(char) and ord(char) <= ord(u'\U0000FAFF'):
        return True

    # CJK Compatibility Forms (FE30–FE4F)
    if ord(u'\U0000FE30') <= ord(char) and ord(char) <= ord(u'\U0000FE4F'):
        return True

    # Range U+FF65–FFDC encodes halfwidth forms, of Katakana and Hangul characters
    if ord(u'\U0000FF65') <= ord(char) and ord(char) <= ord(u'\U0000FFDC'):
        return True

    # Supplementary Ideographic Plane 20000–2FFFF
    if ord(u'\U00020000') <= ord(char) and ord(char) <= ord(u'\U0002FFFF'):
        return True

    return False


def normalize(string, form='NFKC'):
    # For more information about 'NF*', please refer to Unicode equivalence(https://en.wikipedia.org/wiki/Unicode_equivalence)
    assert form in {'NFC', 'NFKC', 'NFD', 'NFKD'}, f'Do not support this kind of form: \'{form}\'!'
    string = unicodedata.normalize(form, string)
    for special_char, normal_char in constant.SPECIAL_TO_NORMAL.items():
        string = re.sub(special_char, normal_char, string)
    return ' '.join(string.split())
