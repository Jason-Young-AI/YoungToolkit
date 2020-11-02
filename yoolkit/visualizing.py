#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) Jason Young (杨郑鑫).
#
# E-Mail: <AI.Jason.Young@outlook.com>
# 2020-10-30 11:18
#
# This source code is licensed under the WTFPL license found in the
# LICENSE file in the root directory of this source tree.


import os
import json
import visdom

from yoolkit.cio import mk_temp


visualizer_dict = dict()


def get_visualizer(name):
    if name in visualizer_dict:
        visualizer = visualizer_dict[name]
    else:
        visualizer = setup_visualizer(name)

    return visualizer


def setup_visualizer(name, server="http://localhost", port=8097,
                  username=None, password=None, logging_path=None, offline=True, overwrite=False):
    visualizer = Visualizer(name, server, port,
        username, password, logging_path, offline, overwrite
    )
    visualizer_dict[name] = visualizer

    return visualizer


class Visualizer(object):
    def __init__(self, name, server, port,
                 username=None, password=None, logging_path=None, offline=False, overwrite=False):
        self.name = name
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.logging_path = logging_path
        self.logging_win_path = self.logging_path + '-win'
        self.offline = offline
        self.overwrite = overwrite
        self.disabled = False
        self.environment = None
        self.windows = set()
        self.window_layout_options = dict(
            height = 300,
            width = 400,
            showlegend = True,
            marginleft = 36,
            marginright = 36,
            margintop = 36,
            marginbottom = 36
        )

    def open(self):
        if self.disabled:
            return
        if self.offline == True:
            if self.logging_path is None:
                self.logging_path = mk_temp('yoolkit-visualizer-', 'file')
            self.environment = visdom.Visdom(env=self.name, log_to_filename=self.logging_path, offline=self.offline)
        else:
            self.environment = visdom.Visdom(
                env=self.name,
                server=self.server, port=self.port,
                username=self.username, password=self.password,
                log_to_filename=self.logging_path
            )
            if self.environment.check_connection() == False:
                import sys
                sys.exit(1)

        if self.logging_path is None:
            return
        else:
            if os.path.isfile(self.logging_path):
                if self.overwrite:
                    with open(self.logging_path, 'w', encoding='utf-8') as logging_file:
                        logging_file.truncate()
            else:
                os.mknod(self.logging_path)

            with open(self.logging_path, 'r', encoding='utf-8') as logging_file:
                for json_entry in logging_file:
                    endpoint, msg = json.loads(json_entry)
                    window_name = self.environment._send(msg, endpoint, from_log=True)
                    self.windows.add(window_name)

            if os.path.isfile(self.logging_win_path):
                if self.overwrite:
                    with open(self.logging_win_path, 'r+', encoding='utf-8') as logging_win_file:
                        for line in logging_win_file:
                            window_name = line.strip()
                            self.environment.close(window_name)
                        logging_win_file.truncate()
            else:
                os.mknod(self.logging_win_path)

            with open(self.logging_win_path, 'w', encoding='utf-8') as logging_win_file:
                for window_name in self.windows:
                    line = window_name + '\n'
                    logging_win_file.writelines(line)

    def close(self):
        if self.disabled:
            return
        if self.environment is None:
            return
        else:
            self.environment.delete_env(self.name)

    def add_window(self, window_name):
        if self.disabled:
            return
        self.windows.add(window_name)
        with open(self.logging_win_path, 'a', encoding='utf-8') as logging_win_file:
            line = window_name + '\n'
            logging_win_file.writelines(line)

    def visualize(self, visualize_type, visualize_name, visualize_title, **keyword_args):
        if self.disabled:
            return
        visualize_method = getattr(self.environment, visualize_type)

        visualize_options = dict()
        visualize_options.update(self.window_layout_options)
        visualize_options.update(keyword_args.get('opts', dict()))
        visualize_options['title'] = visualize_title
        keyword_args['opts'] = visualize_options

        visualize_method(env=self.name, win=visualize_name, **keyword_args)
        self.add_window(visualize_name)

        return visualize_name
