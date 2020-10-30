#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) Jason Young (杨郑鑫).
#
# E-Mail: <AI.Jason.Young@outlook.com>
# 2020-10-30 11:13
#
# This source code is licensed under the WTFPL license found in the
# LICENSE file in the root directory of this source tree.


import numbers


class Statistics(object):
    def __init__(self, structure):
        assert isinstance(structure, set), 'Type of structure should be set().'
        for attribute_name in structure:
            assert isinstance(attribute_name, str), 'Type of {attribute_name} in structure should be str().'
        self.__structure = structure

        for attribute_name in self.structure:
            setattr(self, attribute_name, 0)

    def __str__(self):
        string = str()
        for attribute_name, attribute_value in self:
            string += f'{attribute_name}: {attribute_value} '
        return string

    def __len__(self):
        return len(self.__structure)

    def __setitem__(self, attribute_name, attribute_value):
        if attribute_name not in self.__structure:
            self.__structure.update([attribute_name])
        self.__dict__[attribute_name] = attribute_value

    def __getitem__(self, attribute_name):
        if attribute_name in self.__structure:
            return self.__dict__[attribute_name]
        else:
            return 0

    def __contains__(self, attribute_name):
        return attribute_name in self.structure

    def __iter__(self):
        for attribute_name in self.structure:
            yield (attribute_name, self[attribute_name])

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            result_structure = self.structure
            result_statistics = Statistics(result_structure)
            for attribute_name in self.structure:
                result_statistics[attribute_name] = self[attribute_name] * other
        else:
            result_structure = self.structure & other.structure
            result_statistics = Statistics(result_structure)
            for attribute_name in result_statistics.structure:
                result_statistics[attribute_name] = self[attribute_name] * other[attribute_name]
        return result_statistics

    def __add__(self, other):
        if isinstance(other, numbers.Number):
            result_structure = self.structure
            result_statistics = Statistics(result_structure)
            for attribute_name in self.structure:
                result_statistics[attribute_name] = self[attribute_name] + other
        else:
            result_structure = self.structure | other.structure
            result_statistics = Statistics(result_structure)
            for attribute_name in result_statistics.structure:
                result_statistics[attribute_name] = self[attribute_name] + other[attribute_name]
        return result_statistics

    def __lt__(self, other):
        if isinstance(other, numbers.Number):
            for attribute_name in self.structure:
                if self[attribute_name] >= other:
                    return False
        elif isinstance(other, Statistics):
            if self.structure != other.structure:
                raise ValueError(f"Structure of the operand does not match!")
            else:
                for attribute_name in self.structure:
                    if self[attribute_name] >= other[attribute_name]:
                        return False
        else:
            raise TypeError(f"Wrong type of {other}")
        return True

    def __gt__(self, other):
        if isinstance(other, numbers.Number):
            for attribute_name in self.structure:
                if self[attribute_name] <= other:
                    return False
        elif isinstance(other, Statistics):
            if self.structure != other.structure:
                raise ValueError(f"Structure of the operand does not match!")
            else:
                for attribute_name in self.structure:
                    if self[attribute_name] <= other[attribute_name]:
                        return False
        else:
            raise TypeError(f"Wrong type of {other}")
        return True

    def __eq__(self, other):
        if isinstance(other, numbers.Number):
            for attribute_name in self.structure:
                if self[attribute_name] != other:
                    return False
        elif isinstance(other, Statistics):
            if self.structure != other.structure:
                raise ValueError(f"Structure of the operand does not match!")
            else:
                for attribute_name in self.structure:
                    if self[attribute_name] != other[attribute_name]:
                        return False
        else:
            raise TypeError(f"Wrong type of {other}")
        return True

    def clear(self):
        for attribute_name in self.structure:
            self[attribute_name] = 0

    def max(self):
        max_attribute_value = float('-inf')
        for attribute_name in self.structure:
            if self[attribute_name] > max_attribute_value:
                max_attribute_value = self[attribute_name]
        return max_attribute_value

    @property
    def structure(self):
        return self.__structure
