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


import numpy
import random


from yoolkit.constant import Constant


constant = Constant()
constant.PADDING = '<PAD>'
constant.MATCHING = '<MAT>'
constant.DELETION = '<DEL>'
constant.INSERTION = '<INS>'
constant.SUBSTITUTION = '<SUB>'


"""LevenshteinTool can Calculating Levenshtein-Distance, Printing Manipulation-Sequence, Aligned-Sequences and so on

Levenshtein-Distance(L-Distance, LD) is a measure of the similarity between two sequences, which we will refer to as the reference sequence (ref) and the hypothesis sequence (hyp).

L-Distance is the number of three type manipulations which is required to transform source to target. If the elements of two sequences is the same, we also call this as a kind of manipulation -- matching.

These manipulations is:

    insertions - <INS> ;
    substitutions - <SUB> ;
    deletions - <DEL> ; 
    matching - <MAT> .

This tool can also give the aligned source and target with manipulation-Sequence, we call these as Aligned-Sequences.

    Example:

    Input:
        source: ['t', 'e', 'n', 't']
        target: ['t', 'e', 's', 't', '!']

    Output:
        Levenshtein-Distance: 1
        Manipulation-Sequence: ['<MAT>', '<MAT>', '<SUB>', '<MAT>', '<INS>']
        Aligned-Sequences:
            aligned-source:    ['t', 'e', 'n', 't', '<PAD>']
            aligned-target:    ['t', 'e', 's', 't', '!']

Note:
    Levenshtein-Distance is also sometimes called Edit-Distance.
"""


class Levenshtein(object):
    def __init__(self,
        deletion_weight=1, insertion_weight=1, substitution_weight=1,
        mat_prob=0.25, del_prob=0.25, ins_prob=0.25, sub_prob=0.25
    ):
        self.deletion_weight = deletion_weight
        self.insertion_weight = insertion_weight
        self.substitution_weight = substitution_weight
        self.manipulation_choice_probabilities = {
            constant.MATCHING : mat_prob,
            constant.DELETION : del_prob,
            constant.INSERTION : ins_prob,
            constant.SUBSTITUTION : sub_prob
        }

    def calculate_stage_matrix(self, source, target):
        stage_matrix_size = (len(source) + 1, len(target) + 1)
        stage_matrix = numpy.zeros(stage_matrix_size, dtype=numpy.uint)

        stage_matrix[:,0] = numpy.arange(stage_matrix_size[0])
        stage_matrix[0,:] = numpy.arange(stage_matrix_size[1])

        for source_stage_index in range(1, stage_matrix_size[0]):
            for target_stage_index in range(1, stage_matrix_size[1]):
                source_index = source_stage_index - 1
                target_index = target_stage_index - 1
                if source[source_index] == target[target_index]:
                    #Matching
                    stage_matrix[source_stage_index, target_stage_index] = stage_matrix[source_stage_index-1, target_stage_index-1]
                else:
                    deletion = stage_matrix[source_stage_index-1, target_stage_index] #Deletion
                    insertion = stage_matrix[source_stage_index, target_stage_index-1] #Insertion
                    substitution = stage_matrix[source_stage_index-1, target_stage_index-1] #Substitution
                    stage_matrix[source_stage_index, target_stage_index] = min(
                        deletion + self.deletion_weight,
                        insertion + self.insertion_weight,
                        substitution + self.substitution_weight
                    )

        return stage_matrix

    def backtrack_manipulation_sequence(self, source, target, stage_matrix):
        manipulation_sequence = []
        x, y = len(source), len(target)
        while x != 0 or y != 0:
            candidate_actions = []
            choice_probs = []
            if x>0 and y>0:
                if stage_matrix[x, y] == stage_matrix[x-1, y-1]:
                    if source[x-1] == target[y-1]:
                        candidate_actions.append(constant.MATCHING) #Matching
                        choice_probs.append(self.manipulation_choice_probabilities[constant.MATCHING])
                elif stage_matrix[x, y] == (stage_matrix[x-1, y-1] + self.substitution_weight):
                    candidate_actions.append(constant.SUBSTITUTION) #Substitution
                    choice_probs.append(self.manipulation_choice_probabilities[constant.SUBSTITUTION])
            if x>0:
                if stage_matrix[x, y] == (stage_matrix[x-1, y] + self.deletion_weight):
                    candidate_actions.append(constant.DELETION) #Deletion
                    choice_probs.append(self.manipulation_choice_probabilities[constant.DELETION])
            if y>0:
                if stage_matrix[x, y] == (stage_matrix[x, y-1] + self.insertion_weight):
                    candidate_actions.append(constant.INSERTION) #INSERTION
                    choice_probs.append(self.manipulation_choice_probabilities[constant.INSERTION])

            choice_prob_sum = sum(choice_probs)
            choice_probs = [choice_prob/choice_prob_sum for choice_prob in choice_probs]
            action_index = numpy.random.choice(len(candidate_actions), 1, choice_probs)[0]
            action = candidate_actions[action_index]

            if action == constant.MATCHING:
                manipulation_sequence.append(constant.MATCHING)
                x, y = x - 1, y - 1
            elif action == constant.SUBSTITUTION:
                manipulation_sequence.append(constant.SUBSTITUTION)
                x, y = x - 1, y - 1
            elif action == constant.DELETION:
                manipulation_sequence.append(constant.DELETION)
                x = x - 1
            elif action == constant.INSERTION:
                manipulation_sequence.append(constant.INSERTION)
                y = y - 1

        manipulation_sequence = manipulation_sequence[::-1]

        return manipulation_sequence

    def align_source_and_target(self, source, target, manipulation_sequence):
        source_index = 0
        target_index = 0
        aligned_source = []
        aligned_target = []
        for action in manipulation_sequence:
            if action == constant.MATCHING or action == constant.SUBSTITUTION:
                aligned_source.append(source[source_index])
                aligned_target.append(target[target_index])
                source_index, target_index = source_index + 1, target_index + 1

            elif action == constant.DELETION:
                aligned_source.append(source[source_index])
                aligned_target.append(constant.PADDING)
                source_index = source_index + 1

            elif action == constant.INSERTION:
                aligned_source.append(constant.PADDING)
                aligned_target.append(target[target_index])
                target_index = target_index + 1

        return aligned_source, aligned_target

    def get_levenshtein_distance(self, source, target):
        stage_matrix = self.calculate_stage_matrix(source, target)
        return stage_matrix[-1, -1]

    def get_manipulation_sequence(self, source, target):
        stage_matrix = self.calculate_stage_matrix(source, target)
        manipulation_sequence = self.backtrack_manipulation_sequence(source, target, stage_matrix)
        return manipulation_sequence

    def get_aligned_sequences(self, source, target):
        stage_matrix = self.calculate_stage_matrix(source, target)
        manipulation_sequence = self.backtrack_manipulation_sequence(source, target, stage_matrix)
        aligned_source, aligned_target = self.align_source_and_target(source, target, manipulation_sequence)
        return dict(
            aligned_source=aligned_source,
            aligned_target=aligned_target,
            manipulation=manipulation_sequence
        )
