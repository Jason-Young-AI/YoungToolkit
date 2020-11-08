#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) Jason Young (杨郑鑫).
#
# E-Mail: <AI.Jason.Young@outlook.com>
# 2020-10-30 11:10
#
# This source code is licensed under the WTFPL license found in the
# LICENSE file in the root directory of this source tree.


import io
import os
import pickle
import tempfile
import itertools


def mk_temp(prefix, temp_type, location=tempfile.gettempdir()):
    assert temp_type in set({'dir', 'file'}), f'Invalid temp type: {temp_type} (Options: (\'dir\', \'file\'))'
    assert os.path.isdir(location), f'Location: {location} is not a directory!'
    if temp_type == 'dir':
        temp_path = tempfile.mkdtemp(dir=location, prefix=prefix)

    if temp_type == 'file':
        _, temp_path = tempfile.mkstemp(dir=location, prefix=prefix)

    return temp_path


def rm_temp(temp_path):
    if os.path.isfile(temp_path):
        os.remove(temp_path)

    if os.path.isdir(temp_path):
        for child_temp_path in os.listdir(temp_path):
            rm_temp(child_temp_path)
        os.rmdir(temp_path)


def dump_data(file_path, data_object):
    with open(file_path, 'wb') as file_object:
        pickle.dump(data_object, file_object)


def load_data(file_path):
    with open(file_path, 'rb') as file_object:
        return pickle.load(file_object)


def dump_datas(file_path, data_objects):
    with open(file_path, 'wb') as file_object:
        for data_object in data_objects:
            pickle.dump(data_object, file_object)


def load_datas(file_path):
    with open(file_path, 'rb') as file_object:
        while True:
            try:
                yield pickle.load(file_object)
            except EOFError:
                break


def load_plain(file_path, file_encoding='utf-8', newline='\n', partition_unit='line', partition_size=1000000):
    assert partition_unit in {'byte', 'line'}, f'Invalid unit of partition: \'{partition_unit}\' (Ops: [\'byte\', \'line\'])'
    assert partition_size > 0, f'Invalid size of partition: \'{partition_size}\''

    if partition_unit == 'byte':
        with open(file_path, 'rb') as file_object:
            while True:
                file_partition = file_object.readlines(partition_size)
                if len(file_partition) == 0:
                    break
                else:
                    yield file_partition

    elif partition_unit == 'line':
        with open(file_path, 'r', encoding=file_encoding, newline=newline) as file_object:
            while True:
                file_partition = list(itertools.islice(file_object, partition_size))
                if len(file_partition) == 0:
                    break
                else:
                    yield file_partition

            # # [Attention]: The method below is a few second slower than 'islice' method.
            # file_partition = list()
            # for line in file_object:
            #     file_partition.append(line)
            #     if len(file_partition) == partition_size:
            #         yield file_partition
            #         file_partition = list()
            # if len(file_partition) != 0:
            #     yield file_partition
