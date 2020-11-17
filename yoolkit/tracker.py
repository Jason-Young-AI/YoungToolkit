#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
#
# Copyright (c) Jason Young (杨郑鑫).
#
# E-Mail: <AI.Jason.Young@outlook.com>
# 2020-11-17 11:37
#
# This source code is licensed under the WTFPL license found in the
# LICENSE file in the root directory of this source tree.


import gc
import torch
import numpy
import pynvml
import inspect
import datetime

from yoolkit.cio import mk_temp


byte_size_dict = {
    torch.bool: 1,
    torch.uint8: 1,
    torch.int8: 1,
    torch.int16: 2,
    torch.int32: 4,
    torch.int64: 8,
    torch.float16: 2,
    torch.float32: 4,
    torch.float64: 8,
}



class Tracker(object):
    def __init__(self, path='', verbose=False):
        self.path = path
        if self.path == '':
            self.path = mk_temp('yoolkit-tracker-', 'file')

        self.verbose = verbose

        self.last_tensor_infos = set()

    def setup(self, frame):
        assert inspect.isframe(frame), f'#1 Argument should be a Frame object.'
        self.frame = frame

    @property
    def file_name(self):
        file_name = self.frame.f_globals["__file__"]
        if file_name.endswith(".pyc") or file_name.endswith(".pyo"):
            file_name = file_name[:-1]
        return file_name

    @property
    def module_name(self):
        return self.frame.f_globals["__name__"]

    @property
    def method_name(self):
        return self.frame.f_code.co_name

    @property
    def line_number(self):
        return self.frame.f_lineno

    def get_tensors(self):
        for tracked_object in gc.get_objects():
            try:
                if (torch.is_tensor(tracked_object) or
                    (hasattr(tracked_object, 'data') and torch.is_tensor(tracked_object.data))
                ):
                    if tracked_object.is_cuda:
                        yield tracked_object
                else:
                    continue
            except Exception as e:
                if self.verbose:
                    print('A trivial exception occured: {}'.format(e))

    def track(self, message='', device=0):
        assert self.frame is not None, f'Setup Tracker First!'
        pynvml.nvmlInit()

        handle = pynvml.nvmlDeviceGetHandleByIndex(device)
        meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)

        position = f'{self.module_name} {self.method_name}: line {self.line_number}'

        with open(self.path, 'a+') as f:
            f.write(f'Message: {message}\n')
            tensor_sizes = [tensor.size() for tensor in self.get_tensors()]
            tensor_infos = set()
            for tensor in self.get_tensors():
                tensor_type = type(tensor)
                tensor_shape = tuple(tensor.size())
                tensor_number = tensor_sizes.count(tensor.size())
                tensor_memory = numpy.prod(numpy.array(tensor.size())) * byte_size_dict[tensor.dtype]/1024/1024
                tensor_infos.add((tensor_type, tensor_shape, tensor_number, tensor_memory))

            for t, s, n, m in tensor_infos - self.last_tensor_infos:
                f.write(f'+ | {str(n)} * Size:{str(s):<20} | Memory: {str(m*n)[:6]} M | {str(t):<20}\n')
            for t, s, n, m in self.last_tensor_infos - tensor_infos:
                f.write(f'- | {str(n)} * Size:{str(s):<20} | Memory: {str(m*n)[:6]} M | {str(t):<20}\n')
            self.last_tensor_infos = tensor_infos

            f.write(f"\nAt {position:<50}"
                    f"Total Used Memory:{meminfo.used/1000**2:<7.1f}Mb\n\n")

        pynvml.nvmlShutdown()
