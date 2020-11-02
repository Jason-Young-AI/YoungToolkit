#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) Jason Young (杨郑鑫).
#
# E-Mail: <AI.Jason.Young@outlook.com>
# 2020-11-02 02:19
#
# This source code is licensed under the WTFPL license found in the
# LICENSE file in the root directory of this source tree.


import multiprocessing


def count_cpu():
    return multiprocessing.cpu_count()


def estimate_chunksize(iterator_length=None, factor=4):
    if iterator_length is None:
        chunksize = 1
    else:
        number_worker = count_cpu()

        quotient, remainder = divmod(iterator_length, number_worker * factor)

        if remainder == 0:
            chunksize = quotient
        else:
            chunksize = quotient + 1

    return chunksize


def multi_process(method, iterator, number_worker):
    process_results = list()
    with multiprocessing.Pool(number_worker) as pool:
        async_processes = list()
        for item in iterator:
            async_process = pool.apply_async(method, (item,))
            async_processes.append(async_process)

        for async_process in async_processes:
            process_results.append(async_process.get())
    return process_results
