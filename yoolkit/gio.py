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
import torch


def dumps(data):
    serailized_data = None
    bytes_storage = io.BytesIO()
    torch.save(data, bytes_storage)
    serialized_data = bytes_storage.getvalue()
    return serialized_data


def loads(serialized_data):
    data = None
    bytes_storage = io.BytesIO(serialized_data)
    data = torch.load(bytes_storage)
    return data
