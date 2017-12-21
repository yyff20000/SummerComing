#!/bin/sh

while true
do
    ps -ef | grep "main.py" | grep -v "grep"
    if [ "%?" -eq 1]
    then
        nohup python2.7 main.py &
        echo "process restarted!"
    else
        echo "process already started!"
    fi
    sleep 10
done