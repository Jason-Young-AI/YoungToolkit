#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) Jason Young (杨郑鑫).
#
# E-Mail: <AI.Jason.Young@outlook.com>
# 2020-10-30 11:16
#
# This source code is licensed under the WTFPL license found in the
# LICENSE file in the root directory of this source tree.


import time

from yoolkit.constant import Constant


constant = Constant()
constant.INIT = 'Initial'
constant.ACTI = 'Active'
constant.SUSP = 'Suspend'


class Timer(object):

    INIT_ST = constant.INIT
    ACTI_ST = constant.ACTI
    SUSP_ST = constant.SUSP

    TIMER_STS = [INIT_ST, ACTI_ST, SUSP_ST]

    def __init__(self):
        self.reset()

    @property
    def status(self):
        return self._status

    @property
    def elapsed_time(self):
        if self._status == Timer.INIT_ST:
            return 0
        if self._status == Timer.SUSP_ST:
            return self._elapsed_time
        if self._status == Timer.ACTI_ST:
            return self._elapsed_time + time.perf_counter() - self._time

    @property
    def lap_records(self):
        return self._elapsed_lap_times

    def launch(self):
        current_time = time.perf_counter()
        if self._status != Timer.INIT_ST:
            return
        self._time = current_time
        self._lap_time = current_time

        self._status = Timer.ACTI_ST

    def restart(self):
        current_time = time.perf_counter()

        status_time = self.elapsed_time
        if self._status != Timer.SUSP_ST:
            return status_time
        self._time = current_time
        self._lap_time = current_time

        self._status = Timer.ACTI_ST
        return status_time

    def standby(self):
        current_time = time.perf_counter()

        if self._status != Timer.ACTI_ST:
            return self.elapsed_time

        self._elapsed_time += current_time - self._time
        self._elapsed_lap_time += current_time - self._lap_time
        self._time = current_time
        self._lap_time = current_time

        self._status = Timer.SUSP_ST
        return self.elapsed_time

    def lap(self):
        current_time = time.perf_counter()
        if self._status != Timer.ACTI_ST:
            return self._elapsed_lap_time

        # like standby
        self._elapsed_lap_time += current_time - self._lap_time

        # like restart
        self._lap_time = current_time

        self._elapsed_lap_times.append(self._elapsed_lap_time)
        self._elapsed_lap_time = 0

        return self._elapsed_lap_times[-1]

    def reset(self):
        self._status = Timer.INIT_ST
        self._elapsed_time = 0
        self._elapsed_lap_time = 0
        self._elapsed_lap_times = list()
        self._time = None
        self._lap_time = None
