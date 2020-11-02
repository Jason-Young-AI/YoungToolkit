#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) Jason Young (杨郑鑫).
#
# E-Mail: <AI.Jason.Young@outlook.com>
# 2020-10-30 11:11
#
# This source code is licensed under the WTFPL license found in the
# LICENSE file in the root directory of this source tree.


import logging

from yoolkit.cio import mk_temp


logging_level = dict(
    INFO = logging.INFO,
    WARN = logging.WARN,
    ERROR = logging.ERROR,
    DEBUG = logging.DEBUG,
    FATAL = logging.FATAL,
    NOTSET = logging.NOTSET
)


logger_dict = dict()


def get_logger(name):
    if name in logger_dict:
        logger = logger_dict[name]
    else:
        logger = setup_logger(name)
    return logger


def setup_logger(name, logging_path='', logging_level=logging.NOTSET, to_console=True, to_file=True):
    logging_formatter = logging.Formatter("[%(asctime)s %(levelname)s] %(message)s")
    logger = logging.getLogger(name)
    logger.setLevel(logging_level)

    logger.handlers.clear()

    if to_file:
        if logging_path == '':
            logging_path = mk_temp('yoolkit-logger-', 'file')
            print(f'Logging path is not specified, the following path is used for logging: {logging_path}')

        file_handler = logging.FileHandler(logging_path)
        file_handler.setLevel(logging_level)
        file_handler.setFormatter(logging_formatter)
        logger.addHandler(file_handler)

    if to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging_level)
        console_handler.setFormatter(logging_formatter)
        logger.addHandler(console_handler)
    else:
        print(f'No log report to console, please look throungh logging in \'{logging_path}\'.')

    logger_dict[name] = logger

    return logger
