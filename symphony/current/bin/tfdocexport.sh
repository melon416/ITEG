#!/bin/bash
#
#  COPYRIGHT
#  All Rights Reserved.
#  The copyright notice above does not evidence any actual or intended
#  publication of source code.
#

. ~symphony/current/bin/env.sh
export LD_LIBRARY_PATH=${ORACLE_HOME}/lib

# Drew commented out
#~symphony/current/bin/tfdocexport.py "$@"
#echo ~
~/current/bin/tfdocexport.py "$@"
