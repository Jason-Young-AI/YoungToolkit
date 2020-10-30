#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) Jason Young (杨郑鑫).
#
# E-Mail: <AI.Jason.Young@outlook.com>
# 2020-10-30 11:09
#
# This source code is licensed under the WTFPL license found in the
# LICENSE file in the root directory of this source tree.


import inspect


class BaseDecorator(object):
    def __init__(self):
        pass

    def __call__(self, personal_function):

        def decorator_function(*args, **kargs):
            return personal_function(*args, **kargs)

        return decorator_function


class ArgumentTypeChecker(BaseDecorator):
    def __init__(self, *type_args, **type_kargs):
        super(InstancesChecker, self).__init__()
        self.type_args = type_args
        self.type_kargs = type_kargs

    def __call__(self, personal_function):
        pf_sig = inspect.signature(personal_function)
        names2types = pf_sig.bind_partial(*self.type_args, **self.type_kargs).arguments

        def decorator_function(*value_args, **value_kargs):
            names2values = pf_sig.bind(*value_args, **value_kargs).arguments
            for name, value in names2values.items():
                if name in names2types:
                    types = names2types[name]
                    if not (isinstance(types, list) or isinstance(types, set) or isinstance(types, tuple)):
                        types = [types,]
                    types = list(types)
                    error = True
                    for opt in types:
                        if isinstance(value, opt):
                            error = False
                            break
                    if error:
                        raise TypeError(name)
            return personal_function(*value_args, **value_kargs)

        return decorator_function
