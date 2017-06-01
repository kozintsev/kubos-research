#!/bin/sh
cd `dirname $0` #change to the directory of this script
cd ../kubos

if [ -f /usr/bin/python2 ]; then
    exec "/usr/bin/python2" "__main__.pyw"
else
    # 'python2' does not exist on Debian 7 
    # (see http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=696502 )
    exec "/usr/bin/python" "__main__.pyw"
fi
