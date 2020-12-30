#! /bin/bash
#
# stopv.sh
# Copyright (C) 2020 Jason Young (杨郑鑫) <AI.Jason.Young@outlook.com>
#
# Distributed under terms of the WTFPL license.
#


ps -ef | grep -v grep | grep visdom | awk '{print $2}' | xargs kill -9
