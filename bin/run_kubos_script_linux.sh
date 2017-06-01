#!/bin/sh
cd `dirname $0` #change to the directory of this script
cd ../kubos

if [ -f /usr/bin/python2 ]; then
    exec "/usr/bin/python2" "__main__.pyw" "--mode" "script"
else
    exec "/usr/bin/python" "__main__.pyw" "--mode" "script"
fi
