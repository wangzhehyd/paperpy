#!/bin/bash

#===========================================================
# File Name: server_stop.sh
# Author: wangzhe
# E-mail: wangzhehyd@163.com
# Created Time: 2013-11-24
# Version: 1.0
# Description: 
# Copyright: Chemical Biology Research Center
#===========================================================

PID=`ps -al | grep python | awk '{print $4}'`

if [ "${PID}" != "" ];then
    ./server.py >> server.log &
    echo "Starting the server process!"
else
    echo "Server process is running!"
fi
