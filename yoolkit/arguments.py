#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) Jason Young (杨郑鑫).
#
# E-Mail: <AI.Jason.Young@outlook.com>
# 2020-04-01 20:09
#
# This source code is licensed under the WTFPL license found in the
# LICENSE file in the root directory of this source tree.


import pyhocon
import collections


def load_arguments(hocon_abs_path):
    hocon = pyhocon.ConfigFactory.parse_file(hocon_abs_path)
    return HOCONArguments(hocon)


def update_arguments(arguments, hocon_abs_path):
    assert isinstance(arguments, HOCONArguments), f'Arguments must be a HOCONArguments object.'
    hocon = pyhocon.ConfigFactory.parse_file(hocon_abs_path)
    arguments.update(hocon)
    return arguments


class HOCONArguments(object):
    RESERVED_NAME = set({ '_HOCONArguments__names', 'dictionary', 'hocon', 'update', 'save' })
    def __init__(self, hocon):
        if isinstance(hocon, pyhocon.config_tree.ConfigTree):
            self.__names = []
            for name in hocon:
                if name in HOCONArguments.RESERVED_NAME:
                    raise ValueError(f'Invalid hocon attribute name(\'{name}\')')
                self.__names.append(name)
                if isinstance(hocon[name], pyhocon.config_tree.ConfigTree):
                    setattr(self, name, HOCONArguments(hocon[name]))
                else:
                    setattr(self, name, hocon[name])
        else:
            raise ValueError(f'Argument hocon(\'{hocon}\') is not a \'pyhocon.config_tree.ConfigTree\' object.')

    def __iter__(self):
        for attribute_name in self.__names:
            yield (attribute_name, self[attribute_name])

    def __setitem__(self, attribute_name, attribute_value):
        if attribute_name not in self.__names:
            self.__names.add(attribute_name)
        self.__dict__[attribute_name] = attribute_value

    def __getitem__(self, attribute_name):
        return self.__dict__[attribute_name]

    @property
    def dictionary(self):
        dictionary = {}
        for name in self.__names:
            if isinstance(getattr(self, name), HOCONArguments):
                dictionary[name] = getattr(self, name).dictionary
            else:
                dictionary[name] = getattr(self, name)
        dictionary = collections.OrderedDict(sorted(dictionary.items(), key=lambda x: x[0]))
        return dictionary

    @property
    def hocon(self):
        hocon = pyhocon.ConfigFactory().from_dict(self.dictionary)
        return hocon

    def update(self, hocon):
        if isinstance(hocon, pyhocon.config_tree.ConfigTree):
            for name in hocon:
                if name in HOCONArguments.RESERVED_NAME:
                    raise ValueError(f'Invalid hocon attribute name(\'{name}\')')
                if name not in self.__names:
                    self.__names.append(name)
                if isinstance(hocon[name], pyhocon.config_tree.ConfigTree):
                    if hasattr(self, name):
                        getattr(self, name).update(hocon[name])
                    else:
                        setattr(self, name, HOCONArguments(hocon[name]))
                else:
                    setattr(self, name, hocon[name])
        else:
            raise ValueError(f'Argument hocon(\'{hocon}\') is not a \'pyhocon.config_tree.ConfigTree\' object.')

    def save(self, output_path, output_type='hocon'):
        output_string = pyhocon.converter.HOCONConverter.convert(self.hocon, output_type)
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(output_string)
