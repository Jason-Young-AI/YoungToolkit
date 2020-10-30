#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) Jason Young (杨郑鑫).
#
# E-Mail: <AI.Jason.Young@outlook.com>
# 2020-10-30 11:08
#
# This source code is licensed under the WTFPL license found in the
# LICENSE file in the root directory of this source tree.


class Constant(object):

    class ConstantError(TypeError):
        pass

    class ConstantSetError(ConstantError):
        pass

    class ConstantCaseError(ConstantError):
        pass

    def __setattr__(self, attribute_name, attribute_value):
        if attribute_name in self.__dict__:
            raise ConstantSetError('Cannot change constant \'{}\'!'.format(attribute_name))

        if not attribute_name.isupper():
            raise ConstantCaseError('Constant name \'{}\' must be uppercase!'.format(attribute_name))

        self.__dict__[attribute_name] = attribute_value
