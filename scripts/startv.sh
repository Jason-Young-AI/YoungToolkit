#! /bin/bash
#
# startv.sh
# Copyright (C) 2020 Jason Young (杨郑鑫) <AI.Jason.Young@outlook.com>
#
# Distributed under terms of the WTFPL license.
#


export VISDOM_USERNAME="Jason"
export VISDOM_PASSWORD="123456"
export VISDOM_COOKIE="Guest_Visdom_Cookie"

function start_visdom {
    VISDOM_USE_ENV_CREDENTIALS=1 visdom -port 6789 -enable_login -force_new_cookie;
}

export -f start_visdom

nohup bash -c start_visdom > visdom.log 2>&1 &
